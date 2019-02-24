(ns brygge2.core
  (:import [org.newsclub.net.unix AFUNIXSocketAddress]
           [org.newsclub.net.unix.server AFUNIXSocketServer]
           [java.io File])
  (:require [clojure.tools.logging :as log]
            [cognitect.transit :as transit]
            [clojure.java.io :as io]
            [datomic.client.api :as d])
  (:gen-class))

(def transfer-protocol :msgpack)
(def socket-path "/tmp/brygge.sock")

(defn serve-socket [in out]
  (transit/write (transit/writer out transfer-protocol)
                 (eval (transit/read (transit/reader in transfer-protocol)))))

(defn get-server [socket-address]
  (proxy [AFUNIXSocketServer] [socket-address]
    (doServeSocket [socket]
      (try (let [in (.getInputStream socket) out (.getOutputStream socket)]
        (serve-socket in out)
        (try (.close in) (catch Exception e (log/error e)))
        (try (.close out) (catch Exception e (log/error e)))
        (try (.close socket) (catch Exception e (log/error e))))
      (catch Exception e (log/error e))))))

(defn -main
  [& args]
  (let [socket-address (new AFUNIXSocketAddress (new File socket-path))
        server (get-server socket-address)]
    (.start server)
    (log/info "Started brygge server")))
