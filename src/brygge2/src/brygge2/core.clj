(ns brygge2.core
  (:import [org.newsclub.net.unix AFUNIXServerSocket AFUNIXSocketAddress]
           [org.newsclub.net.unix.demo.server EchoServer]
           [java.io File])
  (:gen-class))


(defn -main
    "I don't do a whole lot ... yet."
    [& args]
    (println "Hello, World!")
    (let [file (new File "/tmp/foo")
          server (AFUNIXServerSocket/newInstance)
          server2 (new EchoServer (new AFUNIXSocketAddress file))
          ]
      (.bind server (new AFUNIXSocketAddress file))
      (prn server)
      (prn server2)
      (.start server2)
    )
    
  )
