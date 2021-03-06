(defproject brygge2 "0.1.0-SNAPSHOT"
  :description "FIXME: write description"
  :url "http://example.com/FIXME"
  :license {:name "EPL-2.0 OR GPL-2.0-or-later WITH Classpath-exception-2.0"
            :url "https://www.eclipse.org/legal/epl-2.0/"}
  :dependencies [[org.clojure/clojure "1.10.0"]
                 [com.kohlschutter.junixsocket/junixsocket-core "2.2.0"]
                 [com.kohlschutter.junixsocket/junixsocket-demo "2.2.0"]
                 [com.kohlschutter.junixsocket/junixsocket-common "2.2.0"]
                 [org.clojure/tools.logging "0.4.1"]
                 [com.datomic/client-pro "0.8.28"]
                 [com.cognitect/transit-clj "0.8.313"]]
  :main ^:skip-aot brygge2.core
  :aot [brygge2.core]
  :target-path "target/%s"
  :profiles {:uberjar {:aot :all}})
