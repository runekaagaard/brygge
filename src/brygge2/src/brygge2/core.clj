(ns brygge2.core
  (:import [org.newsclub.net.unix AFUNIXSocketAddress]
           [org.newsclub.net.unix.server AFUNIXSocketServer]
           [java.io File])
  (:require [clojure.tools.logging :as log]
            ;[datomic.api :as d]
            [cognitect.transit :as transit]
            )
  (:gen-class))

; Catch errors in threads.
(Thread/setDefaultUncaughtExceptionHandler
 (reify Thread$UncaughtExceptionHandler
   (uncaughtException [_ thread ex]
     (log/error ex "Uncaught exception on the thread " (.getName thread)))))

(defn safe-println [& more]
  (.write *out* (str (clojure.string/join " " more) "\n"))
  (flush))

(defn get-server [socket-address]
    (proxy [AFUNIXSocketServer] [socket-address]
    (doServeSocket [socket]
      (let [in (.getInputStream socket) out (.getOutputStream socket)
            reader (transit/reader in :json)]
        (log/info socket in out)
        (log/info (transit/read reader))
        (log/info "FFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
        (.write out "foooo" 0 5)
        (log/info "NNNNNNNNNNNNNNNNNNNNNNNNNNNN")))))

(defn -main
    [& args]
    (let [socket-address (new AFUNIXSocketAddress (new File "/tmp/brygge.sock"))
          server (get-server socket-address)]
      (.start server)
      (println "Running brygge server")
    )
  )
