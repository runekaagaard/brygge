
(ns brygge2.core
  (:import [org.newsclub.net.unix AFUNIXServerSocket AFUNIXSocketAddress]
           [org.newsclub.net.unix.demo.server EchoServer]
           [org.newsclub.net.unix.demo.server DemoServerBase]
           [java.io File]
           ;[brygge2.core Server]
           )
  (:gen-class))

(gen-class
	:name "brygge2.core.Server"
	extends [EchoServer]
	;:init "init"
	;; :constructors {[] []}
	:prefix "server-")

(defn server-doServeSocket [socket]
  nil)

;; public final class EchoServer extends DemoServerBase {
;; 32    public EchoServer(SocketAddress listenAddress) {
;; 33      super(listenAddress);
;; 34    }
;; 35  
;; 36    @Override
;; 37    protected void doServeSocket(Socket socket) throws IOException {
;; 38      int bufferSize = socket.getReceiveBufferSize();
;; 39      byte[] buffer = new byte[bufferSize];
;; 40  
;; 41      try (InputStream is = socket.getInputStream(); //
;; 42          OutputStream os = socket.getOutputStream()) {
;; 43        int read;
;; 44        while ((read = is.read(buffer)) != -1) {
;; 45          os.write(buffer, 0, read);
;; 46        }
;; 47      }
;; 48    }
;; 49  }

(defn -main
    "I don't do a whole lot ... yet."
    [& args]
    (println "Hello, World!")
    (let [file (new File "/tmp/foo")
          server (AFUNIXServerSocket/newInstance)
          server2 (new EchoServer (new AFUNIXSocketAddress file))
          server3 (new brygge2.core.Server (new AFUNIXSocketAddress file))
          ]
      (.bind server (new AFUNIXSocketAddress file))
      (prn server)
      (prn server2)
      ;(.start server2)
      ;(.start server3)
    )
    
  )
