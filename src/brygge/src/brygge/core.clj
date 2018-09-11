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

(defn datom-from-reader [vec]
  ;(apply datomic.db.Datum vec)
  [0, 1, 2, 3, 4]
  )

(def read-handlers
  {
    ;"datascript/DB"    (transit/read-handler db/db-from-reader)
    "datum" (transit/read-handler datom-from-reader) })


(def write-handlers
  {

   ;; DB    (transit/write-handler "datascript/DB"
   ;;          (fn [db]
   ;;            { :schema (:schema db)
   ;;              :datoms (:eavt db) }))
    datomic.db.Datum (transit/write-handler "datum"
        (fn [d]
          ;; (if (.-added d)
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d)]
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d) false]))
          [0, 1, 2, 3, 4]
        ))
    ; datomic.btset.BTSet (get transit/default-write-handlers java.util.List)
    datomic.btset.BTSet (transit/write-handler "btset"
        (fn [d]
          ;; (if (.-added d)
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d)]
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d) false]))
          [0, 1, 2, 3, 4]
        ))
   
    com.datomic.lucene.store.RAMFile (transit/write-handler "ramfile"
        (fn [d]
          ;; (if (.-added d)
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d)]
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d) false]))
          [0, 1, 2, 3, 4]
        ))

   
    clojure.lang.IFn (transit/write-handler "fn"
        (fn [d]
          ;; (if (.-added d)
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d)]
          ;;   [(.-e d) (.-a d) (.-v d) (.-tx d) false]))
          [0, 1, 2, 3, 4]
        ))
   })

(defn result [data & [status]]
    (prn data)
  (let [out (ByteArrayOutputStream. 4096)
        writer (transit/writer out :json
                               ;{:handlers write-handlers}
                               )]
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
  (let [reader (transit/reader (:body req) :json { :handlers read-handlers })
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
  [& args]
    (println "brygge started...")
    (http/start-server handler {:port 8080}))
