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
    [cognitect.transit :as transit]))

(def db-uri "datomic:mem://t1")
(d/create-database db-uri)
(def conn (d/connect db-uri))

(defn result [data]
  (let [out (ByteArrayOutputStream. 4096)
        writer (transit/writer out :json)]
    (prn data)
    (transit/write writer {:content data})
    {:status 200
     :headers {"content-type" "text/plain"}
     :body (.toString out)}))

(defn parse-req [req]
  (let [reader (transit/reader (:body req) :json)
        data (transit/read reader)]
    (prn data)
    (:content data)))

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

;(require '[compojure.api.exception :as ex])
;(require '[ring.util.http-response :as response])

;; (defn custom-handler [f type]
;;   (fn [^Exception e data request]
;;     (f {:message (.getMessage e), :type type})))

;; (api
;;  {:exceptions
;;   {:handlers
;;    {
;;     ::ex/default (custom-handler response/internal-server-error :unknown)}}})

(defn -main
  "I don't do a whole lot ... yet."
  [& args]
    (println "brygge started...")
    (http/start-server handler {:port 8080}))
