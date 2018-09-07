(defproject brygge "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "Eclipse Public License"
            :url "http://www.eclipse.org/legal/epl-v10.html"}
  :dependencies [[aleph "0.4.6"]
                 [gloss "0.2.6"]
                 [compojure "1.6.1"]
                 [org.clojure/clojure "1.9.0"]
                 [org.clojure/core.async "0.4.474"]
                 [com.datomic/datomic-free "0.9.5697"]]
  :main ^:skip-aot brygge.core
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
