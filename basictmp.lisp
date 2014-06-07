(in-package :shop2-user)
;domain and problem for housework tasks including "get" cup and "clean" table service

(defdomain housework 
	(
  	(:operator (!detect ?o ?obj)
               ((at ?o ?obj))
               ((at ?o ?obj))
               ((detected ?obj)(on ?o ?obj))
               );end_!detect
    (:operator (!find ?obj)
  						 ((or(at ?obj ?place)(on ?obj ?place)))
  						 ()
  						 ((found ?obj))
 							 );end_!find		
  	(:operator (!abandon ?obj)
               ((or(at ?obj ?place)(on ?obj ?place))(hold ?obj))
               ((on ?obj ?place)(at ?obj ?place)(hold ?obj)(found ?obj)(graspable ?obj ?obj))
               ()
               );end_!abandon
 		(:operator (!close ?obj_B)
  						 ((or(at ?obj_B ?place)(on ?obj_B ?place))(opened ?obj_B)(reachable ?obj))
  						 ((opened ?obj_B))
  						 ((closed ?obj_B))
 							 )	;end_!close			
		(:operator (!move ?to)
							 ((robot_position ?from))
							 ((robot_position ?from))
							 ((robot_position ?to))
							 )    ;end_!move		
		(:operator (!grasp ?tag)
							 ((graspable ?tar ?obj))
							 ((or(at ?tag ?place)(on ?tag ?place))(found ?tag))
							 ((hold ?tag))
							 )    ;end_!grasp
    (:operator (!release ?obj)
               (or((or(at ?obj ?place)(on ?obj ?place))(hold ?obj))(hold ?obj))
               ((hold ?obj)(on ?obj ?place)(at ?obj ?place)(found ?obj))
               ()
               )    ;end_!release
		(:operator (!pull ?tag)
							 ((hold ?tag)(graspable ?tag ?obj)(closed ?obj))
							 ((closed ?obj))
							 ((opened ?obj))
							 )	;end_!pull	
   
  	(:method (open ?obj)         
             ((reachable ?obj)(closed ?obj)(isContainer ?obj)(graspable ?tag ?obj)(inside ?o ?obj))
             ((!grasp ?tag)(!pull ?tag)(print-current-state)(!release ?tag)(print-current-state))
              )  ;end_open

    (:method (clean ?obj) 
             (not(detected ?obj))
             ((!find ?obj)(!move ?obj)(detect ?obj)(clean ?obj))        
             ((on ?o ?obj)(isTrach ?o)(graspable ?o ?o))
             ((get ?o)(discard ?o trashcan)(clean ?obj)(print-current-state))
             ((on ?o ?obj)(graspable ?o ?o))
             ((get ?o)(put sink)(clean ?obj))
             ()
             ()
             )  ;end_clean
    (:method (discard ?obj trashcan)         
             ((hold ?obj))
             ((!find trashcan)(!move trashcan)(!abandon ?obj))
             )  ;end_discard

    (:method (put ?place)         
             ((hold ?obj))
             ((print-current-state)(!move ?place)(!release ?obj))
              )   ;end_put
    (:method (give ?per ?obj)					
    				 ((or(at ?obj ?place)(on ?obj ?place)) (at ?per ?per_place))
             ((get ?obj)(!find ?per)(put ?per))
             ((inside ?obj ?obj_B) (at ?per ?place))
             ((get ?obj)(!find ?per)(put ?per))
             )	;end_give		  
	  (:method (get ?obj)
    				 ((not (hold ?obj))(found ?obj)(reachable ?obj))
    				 	((!grasp ?obj))    
    				 ((not (hold ?obj))(found ?obj)(or(at ?obj ?place)(on ?obj ?place)))
    				 	((!move ?place)(!grasp ?obj))
    				 ((not (hold ?obj))(or(at ?obj ?place)(on ?obj ?place)))
    				 	((!find ?obj)(!move ?place)(!grasp ?obj)) 
    				 ((not (hold ?obj))(inside ?obj ?obj_B)(or(at ?obj_B ?place)(on ?obj_B ?place))(closed ?obj_B))
						 	((!find ?obj_B)(!move ?place)(search ?obj ?objB)(!grasp ?obj))
  					 );end_get
	  (:method (search ?obj ?objB)
    				 ((not (hold ?obj))(inside ?obj ?obj_B)(or(at ?obj_B ?place)(on ?obj_B ?place))(closed ?obj_B) not(found ?obj_B))
						 ((!find ?obj_B)(open ?obj_B)(!find ?obj))	
             ((not (hold ?obj))(inside ?obj ?obj_B)(or(at ?obj_B ?place)(on ?obj_B ?place))(closed ?obj_B))
             ((open ?obj_B)(print-current-state)(!find ?obj))
  					 )  ;end_search        
 		(:method (detect ?obj)             
             ((at ?o ?obj))
             ((print-current-state)(!detect ?o ?obj)(detect ?obj))
             ()
             ()
             );end_detect
    (:method (print-current-state)
             ((eval (print-current-state)))
             ()
             );end_print-current-state
    (:method (test)
             ()
             ((clean table))  
             ) ;end_test

  	(:-(reachable ?obj)
  		  yes
  		 ((or(at ?obj ?place)(on ?obj ?place))(robot_position ?place)(same ?place ?place))
  		 )  
  	(:-(at ?o ?obj)
        yes
       ((opened ?obj)(inside ?o ?obj))
       )  
    (:- (same ?x ?x)
 			  nil
 			 )
    (:- (different ?x ?y)
    	 ((not (same ?x ?y)))
    	 )
	)
);defdomain housework end

(defproblem problem housework
  ;;;initial state;;;
  (
  	(robot_position liveroom)
    (at me liveroom)
    (inside cup cupboard)
    (closed cupboard)
    (at cupboard table)
  	(isContainer cupboard)
    (graspable handle cupboard)
    (graspable cup cup)
    (graspable cup1 cup1)
    (graspable cup2 cup2)
    (graspable beer beer)
    (at table kitchen)
    ;(at cup table)
    (at cup1 table)
    ;(on cup1 table)
    ;(on beer table)
    ;(on cup2 table)
    (isTrach beer)
    (at cup2 table)
    (at beer table)
    
    (at trashcan kitchen)
  	;(found cup)
    ;(robot_position table)
  	;(at apple cesspit)
  	;(size cup 1)
  	;(size banjo 1)
  	;(size cupboard 100) 
  	
        
  )
 ;;;action;;;
  (
  	;(find cup)
  	;(!move kitchen)
    ;(test)
    ;(clean table)
  )
)

;(print-current-state)
;(shop-trace chean)
(find-plans 'problem :verbose :plans :which :first)

;(find-plans 'problem :verbose :plans :which :all)
