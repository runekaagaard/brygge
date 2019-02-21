
(ns brygge2.core
  (:import [org.newsclub.net.unix AFUNIXServerSocket AFUNIXSocketAddress]
           [org.newsclub.net.unix.server AFUNIXSocketServer]
           [java.net SocketAddress]
           [java.io File])
  (:gen-class))

(defn safe-println [& more]
  (.write *out* (str (clojure.string/join " " more) "\n")))

(defn get-server [socket-address]
    (proxy [AFUNIXSocketServer] [socket-address]
    (doServeSocket [socket]
        (prn "abc")
      )))

(defn -main
    [& args]
    (let [socket-address (new AFUNIXSocketAddress (new File "/tmp/foo"))
          server (get-server socket-address)]
      (.start server)
      (prn "Running")
    )
  )
