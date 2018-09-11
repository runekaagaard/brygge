(ns brygge.core
  (:import
    [io.netty.handler.ssl SslContextBuilder]
    [java.io ByteArrayInputStream ByteArrayOutputStream])
  (:require
    [compojure.core :as compojure :refer [GET POST]]
    [ring.middleware.params :as params]
    [compojure.route :as route]
    [compojure.response :refer [Renderable]]
    [aleph.http :as http]
    [byte-streams :as bs]
    [manifold.stream :as s]
    [manifold.deferred :as deferred]
    [clojure.core.async :as a]
    [clojure.java.io :refer [file]]
    [aleph.http :as http]
    [datomic.api :as d]
    [cognitect.transit :as transit]
    [clojure.string :as str]))

(defn result [data & [status]]
  (let [out (ByteArrayOutputStream. 4096)
        writer (transit/writer out :json)]
    (transit/write writer {:content data})
    {:status (or status 200)
     :headers {"content-type" "text/plain"}
     :body (.toString out)}))

(defn wrap-exception [handler]
  (fn [request]
    (try (handler request)
      (catch Exception e
        (result (with-out-str (clojure.stacktrace/print-stack-trace e 100)) 500)))))

(def conn
  (memoize
   (fn [db-uri]
    (d/connect db-uri))))


(defn parse-req [req]
  (let [reader (transit/reader (:body req) :json)
        data (transit/read reader)]
    (:content data)))

(defn insert-db [x]
  (if (and (string? x ) (str/starts-with? x "datomic:"))
    (d/db (conn x))
    x))

(defn insert-connection [x]
  (if (and (string? x ) (str/starts-with? x "datomic:"))
    (conn x)
    x))

(defn format-tx [data]
  {:db-before (last (str/split (pr-str (:db-before data)) #"@"))
   :db-after (last (str/split (pr-str (:db-after data)) #"@"))
   :tempids (:tempids data)
   :tx-data (for [x (:tx-data data)] [(.e x) (.a x) (.v x) (.tx x) (.added x)])})

(defn create-database-handler [req]
  (result (d/create-database (parse-req req))))

(defn transact-handler [req]
  (let [args (map insert-connection (parse-req req))]
    (result (format-tx @(apply d/transact args)))))

(defn query-handler [req]
  (let [args (map insert-db (parse-req req))]
    (result (apply d/q args))))

(def handler
  (params/wrap-params
   (wrap-exception
    (compojure/routes
      (POST "/transact"         [] transact-handler)
      (POST "/query"         [] query-handler)
      (POST "/create-database"         [] create-database-handler)
      (route/not-found "No such page.")))))

(defn -main
  "Starts the server."
  [port]
    (http/start-server handler {:port (Integer. port)})
    (println "brygge started on port" port))
