(ns brygge2.core
  (:import [org.newsclub.net.unix AFUNIXServerSocket AFUNIXSocketAddress]
           [org.newsclub.net.unix.server AFUNIXSocketServer]
           [java.net SocketAddress]
           [java.io File])
  (:require [clojure.tools.logging :as log])
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
      (safe-println socket))))

(defn -main
    [& args]
    (let [socket-address (new AFUNIXSocketAddress (new File "/tmp/brygge.sock"))
          server (get-server socket-address)]
      (.start server)
      (println "Running brygge server")
    )
  )
