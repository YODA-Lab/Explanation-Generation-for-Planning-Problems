(define (problem BLOCKS-4-0)
(:domain BLOCKS)
(:objects B A - block)
(:init (CLEAR A) (CLEAR B) (ONTABLE A) (ONTABLE B) (HANDEMPTY))
(:goal (and (ON B A))))