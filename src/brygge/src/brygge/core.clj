(ns brygge.core
  (:import
    [io.netty.handler.ssl SslContextBuilder])
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
    [clojure.java.io :refer [file]]))


(require '[aleph.http :as http])
(require '[datomic.api :as d])
(require '[cognitect.transit :as transit])
(import [java.io ByteArrayInputStream ByteArrayOutputStream])

(def  uri "datomic:free://localhost:4334/t1")
(d/create-database uri)
(def conn (d/connect uri))

(defn result [data]
  (let [out (ByteArrayOutputStream. 4096)
        writer (transit/writer out :json)]
    (println (pr-str) data)
    (transit/write writer data)
    {:status 200
     :headers {"content-type" "text/plain"}
     :body (.toString out)}))

(defn parse-req [req]
  (let [reader (transit/reader (:body req) :json)
        data (transit/read reader)]
    (println (pr-str data))
    data))

(defn transact-handler [req]
   (result (pr-str @(d/transact conn (parse-req req)))))

(defn query-handler [req]
  (let [db (d/db conn)]
    (result (d/q (parse-req req) db))
  ))

(def handler
  (params/wrap-params
    (compojure/routes
      (POST "/transact"         [] transact-handler)
      (POST "/query"         [] query-handler)
      (route/not-found "No such page."))))

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
    (println "brygge started...")
    (http/start-server handler {:port 8080}))
