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

(defn parse-req [req]
  (let [reader (transit/reader (:body req) :json)]
    (println (transit/read reader))))

(defn transact-handler [req]
  {:status 200
   :headers {"content-type" "text/plain"}
   :body (str (d/transact conn (parse-req req)))})

(defn query-handler [req]
  (let [db (d/db conn)]
  {:status 200
   :headers {"content-type" "text/plain"}
   :body (str (d/q (parse-req req) db))}))

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
