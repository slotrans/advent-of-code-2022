(ns net.blergh.aoc2022 
    (:require [clojure.string :as str])
)

(defn chunk-input [input-str]
    (let [chunks (str/split input-str #"\n\n")]
        (for [c chunks]
            (vec (str/split c #"\n"))
        )
    )
)

(defn total-calories-of-a-chunk [chunk]
    (apply
        +
        (for [snack chunk]
            (Integer/parseInt snack)
        )
    )
)

(defn calories-per-elf [input-str]
    (map 
        total-calories-of-a-chunk
        (chunk-input input-str)
    )
)

(defn total-for-top-three [cals-per-elf]
    (->> cals-per-elf
        (sort)
        (reverse)
        (take 3)
        (apply +)
    )
)



(def input01 (slurp "../input/input01"))

(def max-calories (apply max (calories-per-elf input01)))
(println (str "(p1 answer) most calories held by an elf: " max-calories))

(def top3 (total-for-top-three (calories-per-elf input01)))
(println (str "(p2 answer) top 3 elves' total calories: " top3))
