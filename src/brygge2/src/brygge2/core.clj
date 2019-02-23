(ns brygge2.core
  (:import [org.newsclub.net.unix AFUNIXSocketAddress]
           [org.newsclub.net.unix.server AFUNIXSocketServer]
           [java.io File])
  (:require [clojure.tools.logging :as log]
            ;[datomic.api :as d]
            [cognitect.transit :as transit]
            [clojure.java.io :as io]
  )
  (:gen-class))

(def transfer-protocol :msgpack)

(defn get-server [socket-address]
    (proxy [AFUNIXSocketServer] [socket-address]
    (doServeSocket [socket]
      (try (let [in (.getInputStream socket) out (.getOutputStream socket)
                 reader (transit/reader in transfer-protocol)
                 writer (transit/writer out transfer-protocol)]
        (transit/write writer (transit/read reader))
        (try (.close in) (catch Exception e (log/error e)))
        (try (.close out) (catch Exception e (log/error e)))
        (try (.close socket) (catch Exception e (log/error e))))
      (catch Exception e (log/error e))))))

(defn -main
    [& args]
    (let [socket-address (new AFUNIXSocketAddress (new File "/tmp/brygge.sock"))
          server (get-server socket-address)]
      (.start server)
      (println "Running brygge server")
    )
  )
