personal_injury_taxonomy = {

    # 1. Motor Vehicle Accidents
    'motor_vehicle_accidents': {
        'car_accidents': [
            # Core terms
            'car accident', 'auto accident', 'automobile accident', 'vehicle collision', 'car crash', 
            'motor vehicle accident', 'mvc', 'car wreck', 'auto wreck', 'vehicle wreck',
            'fender bender', 'minor car accident', 'vehicle incident',
            
            # Intent-specific (injury context)
            'injured in car accident', 'hurt in car crash', 'car accident injury', 'auto accident injury',
            'car accident victim', 'auto accident victim', 'vehicle accident victim', 'injured driver',
            'injured passenger', 'car accident personal injury', 'auto accident claim',
            
            # Collision types
            'rear end collision', 'rear-end collision', 'rear end accident', 'rear-end accident',
            'head on collision', 'head-on collision', 'head on crash', 'head-on crash',
            'side impact collision', 'side impact accident', 't-bone accident', 't-bone collision',
            'rollover accident', 'rollover crash', 'rollover collision', 'car rolled over',
            'multi-car accident', 'multi-vehicle accident', 'multiple car accident',
            'chain reaction accident', 'pileup accident', 'pile-up accident',
            
            # Location-specific
            'highway accident', 'freeway accident', 'interstate accident', 'expressway accident',
            'intersection accident', 'traffic light accident', 'stop sign accident', 'parking garage accident',
            
            # Fault indicators (PI context)
            'not at fault accident', 'other driver fault', 'someone hit my car', 'hit by another car',
            'other driver hit me', 'rear ended by another car', 'sideswiped by another car',
            'non-intoxicated car accident', 'non-DUI car accident', 'sober driver accident',
            'other driver ran red light', 'other driver ran stop sign',
            
            # Severity indicators
            'serious car accident', 'severe car accident', 'major car accident', 'bad car accident',
            'devastating car accident', 'catastrophic car accident',
            
            # Common phrases
            'car accident lawyer needed', 'need car accident attorney', 'car accident settlement',
            'car accident compensation', 'car accident damages',
            
            # Variations and misspellings
            'car accidnet', 'auto accidnet', 'vehical accident', 'automible accident'
        ],
        
        'motorcycle_accidents': [
            # Core terms
            'motorcycle accident', 'motorcycle crash', 'motorcycle wreck', 'motorcycle collision',
            'motorbike accident', 'motorbike crash', 'motorcycle incident', 'mc accident',
            
            # Intent-specific (injury context)
            'motorcycle accident injury', 'injured in motorcycle accident', 'hurt in motorcycle crash',
            'motorcycle accident victim', 'motorcycle rider injured', 'motorcyclist injured',
            'motorcycle accident personal injury', 'motorcycle accident claim',
            
            # Collision types
            'motorcycle vs car', 'motorcycle hit by car', 'car hit motorcycle',
            'motorcycle rear ended', 'motorcycle sideswiped', 'motorcycle t-boned',
            'motorcycle head on collision', 'motorcycle rollover', 'motorcycle laid down',
            'motorcycle lowside', 'motorcycle highside',
            
            # Fault indicators
            'not at fault motorcycle accident', 'other driver hit motorcycle', 'car hit my motorcycle',
            'motorcycle accident other driver fault', 'driver didnt see motorcycle',
            'motorcycle right of way accident',
            
            # Severity indicators
            'serious motorcycle accident', 'severe motorcycle accident', 'major motorcycle accident',
            'catastrophic motorcycle accident', 'fatal motorcycle accident',
            
            # Motorcycle-specific issues
            'motorcycle visibility accident', 'motorcycle lane splitting accident', 'motorcycle filtering accident',
            'motorcycle road hazard accident', 'motorcycle pothole accident',
            
            # Legal phrases
            'motorcycle accident lawyer', 'motorcycle accident attorney', 'motorcycle accident settlement',
            'motorcycle accident compensation',
            
            # Vehicle types
            'harley davidson accident', 'sport bike accident', 'cruiser motorcycle accident',
            'touring motorcycle accident', 'dirt bike accident', 'scooter accident',
            
            # Variations and misspellings
            'motorcyle accident', 'motercycle accident', 'motor cycle accident'
        ],
        
        'truck_accidents': [
            # Core terms
            'truck accident', 'truck crash', 'truck wreck', 'truck collision', 'trucking accident',
            '18-wheeler', '18 wheeler', 'eighteen wheeler', 'semi truck', 'semi-truck', 'semi accident',
            'semi crash', 'semi wreck', 'big rig', 'big rig accident', 'tractor trailer',
            'tractor-trailer', 'commercial truck',
            
            # Intent-specific (injury context)
            'injured by truck', 'hurt by truck', 'truck accident injury', 'truck accident victim',
            'hit by truck', 'hit by semi', 'hit by 18 wheeler', 'truck accident personal injury',
            'truck accident claim', 'trucking accident injury',
            
            # Collision types
            'truck rear ended me', 'rear ended by truck', 'truck hit my car', 'truck sideswiped me',
            'truck jackknife accident', 'jackknife accident', 'truck rollover', 'truck rollover accident',
            'truck underride accident', 'underride accident', 'truck override accident',
            'truck vs car accident', 'car vs truck accident',
            
            # Truck-specific issues
            'truck driver fatigue accident', 'truck brake failure', 'truck tire blowout accident',
            'truck mechanical failure', 'truck load shift accident', 'overloaded truck accident',
            'truck blind spot accident', 'truck wide turn accident', 'truck backing accident',
            
            # Fault indicators
            'not at fault truck accident', 'truck driver fault', 'negligent truck driver',
            'truck driver error', 'unsafe truck driver', 'truck company negligence',
            'trucking company liability',
            
            # Severity indicators
            'serious truck accident', 'severe truck accident', 'major truck accident',
            'catastrophic truck accident', 'fatal truck accident', 'devastating truck accident',
            
            # Company types
            'delivery truck accident', 'freight truck accident', 'cargo truck accident',
            'logging truck accident', 'tanker truck accident', 'flatbed truck accident',
            'garbage truck accident', 'dump truck accident',
            
            # Legal phrases
            'truck accident lawyer', 'truck accident attorney', 'trucking accident lawyer',
            'truck accident settlement', 'truck accident compensation', '18 wheeler lawyer',
            
            # Variations and misspellings
            'truck accidnet', 'semi accidnet', '18-wheler', 'tracktor trailer'
        ],
        
        'rideshare_accidents': [
            # Core brand terms
            'uber', 'uber accident', 'uber crash', 'uber wreck', 'uber collision',
            'lyft', 'lyft accident', 'lyft crash', 'lyft wreck', 'lyft collision',
            'rideshare', 'ride sharing', 'ride share', 'rideshare accident', 'rideshare crash',
            'rideshare collision', 'ride sharing accident',
            
            # Intent-specific (injury context)
            'injured in uber', 'injured in lyft', 'hurt in uber', 'hurt in lyft',
            'uber accident injury', 'lyft accident injury', 'rideshare injury', 'rideshare accident injury',
            'uber passenger injured', 'lyft passenger injured', 'rideshare passenger injury',
            'uber driver injured', 'lyft driver injured', 'rideshare driver injury',
            
            # Specific scenarios
            'uber hit my car', 'lyft hit my car', 'hit by uber driver', 'hit by lyft driver',
            'uber rear ended me', 'lyft rear ended me', 'uber sideswiped me', 'lyft sideswiped me',
            'accident while in uber', 'accident while in lyft', 'crash during uber ride', 'crash during lyft ride',
            
            # Fault and liability
            'uber driver fault', 'lyft driver fault', 'negligent uber driver', 'negligent lyft driver',
            'uber company liability', 'lyft company liability', 'rideshare company negligence',
            'uber insurance claim', 'lyft insurance claim', 'rideshare insurance',
            
            # Legal context
            'uber accident lawyer', 'lyft accident lawyer', 'rideshare accident lawyer',
            'uber accident attorney', 'lyft accident attorney', 'rideshare accident attorney',
            'uber accident claim', 'lyft accident claim', 'rideshare accident claim',
            'uber accident settlement', 'lyft accident settlement', 'rideshare settlement',
            'uber accident compensation', 'lyft accident compensation',
            
            # Status-related (important for coverage)
            'uber driver on duty accident', 'lyft driver on duty accident', 'uber app on accident',
            'lyft app on accident', 'uber driver off duty accident', 'lyft driver off duty accident',
            'uber driver with passenger accident', 'lyft driver with passenger accident',
            
            # Other rideshare services
            'via accident', 'juno accident', 'waymo accident', 'rideshare service accident',
            
            # Variations and common phrases
            'ridesharing accident', 'ride-sharing accident', 'ride-share accident',
            'accident with uber', 'accident with lyft', 'rideshare crash victim'
        ],
        
        'delivery_driver_accidents': [
            # Core terms
            'delivery driver accident', 'delivery accident', 'delivery truck accident', 'delivery van accident',
            'delivery vehicle accident', 'commercial delivery accident',
            
            # Food delivery services
            'food delivery accident', 'doordash accident', 'door dash accident', 'uber eats accident',
            'grubhub accident', 'grub hub accident', 'postmates accident', 'instacart accident',
            'food delivery driver accident', 'meal delivery accident',
            
            # Package delivery companies
            'amazon delivery accident', 'amazon driver accident', 'amazon van accident',
            'fedex accident', 'fed ex accident', 'fedex driver accident', 'fedex truck accident',
            'ups accident', 'ups driver accident', 'ups truck accident',
            'usps accident', 'postal service accident', 'mail carrier accident',
            'dhl accident', 'dhl driver accident',
            
            # Intent-specific (injury context)
            'hit by delivery driver', 'hit by delivery truck', 'hit by delivery van',
            'injured by delivery driver', 'hurt by delivery driver', 'delivery driver hit me',
            'delivery accident injury', 'delivery driver accident victim',
            
            # Specific scenarios
            'delivery driver rear ended me', 'delivery truck hit my car', 'delivery van sideswiped me',
            'amazon driver hit me', 'fedex driver hit me', 'ups driver hit me',
            'doordash driver accident', 'uber eats driver crash', 'delivery driver backing accident',
            'delivery driver parking accident', 'delivery driver rushing accident',
            
            # Fault and liability
            'delivery driver fault', 'negligent delivery driver', 'delivery company negligence',
            'amazon delivery negligence', 'fedex driver negligence', 'ups driver negligence',
            'delivery company liability', 'commercial delivery liability',
            
            # Legal context
            'delivery accident lawyer', 'delivery driver accident attorney', 'delivery accident claim',
            'amazon delivery accident lawyer', 'fedex accident attorney', 'ups accident lawyer',
            'delivery accident settlement', 'delivery accident compensation',
            
            # Vehicle types
            'amazon prime van accident', 'fedex ground truck accident', 'ups brown truck accident',
            'delivery box truck accident', 'package delivery vehicle accident',
            
            # Other delivery services
            'grocery delivery accident', 'package delivery accident', 'courier accident',
            'messenger accident', 'same day delivery accident'
        ],
        
        'pedestrian_hit': [
            # Core terms
            'pedestrian accident', 'pedestrian hit', 'pedestrian struck', 'pedestrian collision',
            'hit by car while walking', 'struck by vehicle', 'vehicle hit pedestrian', 'car hit pedestrian',
            'pedestrian vs vehicle', 'pedestrian vs car', 'walker hit by car',
            
            # Location-specific
            'crosswalk accident', 'crosswalk pedestrian accident', 'hit in crosswalk', 'struck in crosswalk',
            'sidewalk accident', 'hit on sidewalk', 'struck on sidewalk', 'parking lot pedestrian accident',
            'intersection pedestrian accident', 'street crossing accident', 'jaywalking accident',
            
            # Intent-specific (injury context)
            'pedestrian injury', 'pedestrian accident injury', 'injured pedestrian', 'hurt while walking',
            'pedestrian accident victim', 'pedestrian trauma', 'pedestrian personal injury',
            
            # Specific scenarios
            'hit and run pedestrian', 'hit and run walker', 'pedestrian hit and run',
            'backup accident pedestrian', 'reversing car hit pedestrian', 'car backing up hit pedestrian',
            'turning car hit pedestrian', 'right turn pedestrian accident', 'left turn pedestrian accident',
            'driveway pedestrian accident', 'school zone pedestrian accident',
            
            # Vehicle types
            'truck hit pedestrian', 'bus hit pedestrian', 'motorcycle hit pedestrian',
            'delivery truck hit pedestrian', 'taxi hit pedestrian', 'uber hit pedestrian',
            
            # Fault indicators
            'driver fault pedestrian accident', 'negligent driver hit pedestrian', 'distracted driver hit pedestrian',
            'speeding driver hit pedestrian', 'drunk driver hit pedestrian', 'texting driver hit pedestrian',
            'driver failed to yield pedestrian', 'driver ran red light hit pedestrian',
            
            # Severity indicators
            'serious pedestrian accident', 'severe pedestrian injury', 'fatal pedestrian accident',
            'catastrophic pedestrian accident', 'pedestrian critically injured',
            
            # Age-specific (vulnerable populations)
            'child pedestrian accident', 'elderly pedestrian accident', 'senior pedestrian hit',
            'disabled pedestrian accident', 'wheelchair pedestrian accident',
            
            # Legal context
            'pedestrian accident lawyer', 'pedestrian accident attorney', 'pedestrian accident claim',
            'pedestrian accident settlement', 'pedestrian accident compensation', 'pedestrian rights',
            
            # Common phrases
            'pedestrian had right of way', 'pedestrian crossing legally', 'pedestrian in crosswalk',
            'pedestrian accident fault', 'who is at fault pedestrian accident'
        ],
        
        'bicycle_accidents': [
            # Core terms
            'bicycle accident', 'cycling accident', 'cyclist accident', 'bicycle crash',
            'bicycle collision', 'bicycle wreck',
            'bicycle incident', 'cycling incident', 'cyclist injured', 'bicyclist injured',
            
            # Electric bike terms
            'e-bike accident', 'ebike accident', 'e bike accident', 'electric bicycle accident',
            'electric bike accident', 'electric bicycle crash', 'e-bike crash', 'ebike crash',
            'electric scooter bicycle', 'electric bike collision',
            
            # Intent-specific (injury context)
            'bicycle accident injury', 'cycling injury', 'cyclist injury',
            'injured while cycling', 'hurt while biking', 'bicycle accident victim', 'cyclist victim',
            'bicycle personal injury',
            
            # Vehicle vs bicycle scenarios
            'car hit bicycle', 'car hit cyclist', 'vehicle hit bicycle',
            'truck hit bicycle', 'bus hit bicycle', 'motorcycle hit bicycle',
            'car vs bicycle', 'vehicle vs bicycle', 'bicycle vs car accident',
            'hit by car while biking', 'struck by car while cycling',
            
            # Specific collision types
            'bicycle rear ended', 'cyclist rear ended',
            'bicycle sideswiped', 'cyclist sideswiped',
            'bicycle doored', 'car door hit bicycle', 'car door bicycle accident',
            'right hook bicycle accident', 'left cross bicycle accident',
            
            # Location-specific
            'bike lane accident', 'bicycle lane accident', 'cycling lane accident',
            'intersection bicycle accident', 'crosswalk bicycle accident', 'sidewalk bicycle accident',
            'bike path accident', 'bicycle trail accident', 'road bicycle accident',
            
            # Fault indicators
            'driver fault bicycle accident', 'negligent driver hit cyclist', 'distracted driver hit bicycle',
            'speeding driver hit cyclist', 'driver failed to see bicycle', 'bicycle right of way accident',
            'driver turned into bicycle', 'unsafe lane change hit bicycle',
            
            # Bicycle-specific issues
            'bicycle helmet accident', 'no helmet bicycle accident', 'bicycle safety accident',
            'bicycle visibility accident', 'bicycle road hazard accident', 'bicycle pothole accident',
            
            # Age and type considerations
            'child bicycle accident', 'adult bicycle accident',
            'mountain bike accident', 'road bike accident', 'commuter bicycle accident',
            
            # Legal context
            'bicycle accident lawyer', 'cycling accident lawyer',
            'bicycle accident claim', 'bicycle accident settlement', 'bicycle accident compensation',
            'cyclist rights', 'bicycle law',
            
            # Severity indicators
            'serious bicycle accident', 'major cycling accident',
            'fatal bicycle accident', 'bicycle accident head injury',
            
            # Common phrases
            'bicycle accident fault', 'who is at fault bicycle accident', 'bicycle traffic laws',
            'bicycle accident statistics'
        ],
        
        'electric_scooter_accidents': [
            # Core terms
            'electric scooter accident', 'e-scooter accident', 'e scooter accident', 'scooter accident',
            'electric scooter crash', 'e-scooter crash', 'e scooter crash', 'scooter crash',
            'electric scooter collision', 'e-scooter collision', 'scooter collision',
            'electric scooter wreck', 'scooter wreck', 'electric scooter incident',
            
            # Brand-specific terms
            'lime scooter accident', 'lime scooter crash', 'lime scooter injury', 'lime accident',
            'bird scooter accident', 'bird scooter crash', 'bird scooter injury', 'bird accident',
            'spin scooter accident', 'razor scooter accident', 'shared scooter accident',
            'rental scooter accident', 'scooter share accident',
            
            # Intent-specific (injury context)
            'electric scooter injury', 'e-scooter injury', 'scooter injury', 'scooter accident injury',
            'injured on electric scooter', 'hurt on e-scooter', 'electric scooter accident victim',
            'scooter rider injured', 'electric scooter personal injury',
            
            # Vehicle vs scooter scenarios
            'car hit electric scooter', 'car hit e-scooter', 'car hit scooter', 'vehicle hit scooter',
            'truck hit electric scooter', 'bus hit scooter', 'car vs electric scooter',
            'hit by car on scooter', 'struck by car on electric scooter',
            
            # Specific collision types
            'electric scooter rear ended', 'e-scooter rear ended', 'scooter sideswiped',
            'electric scooter doored', 'scooter fell off', 'electric scooter thrown off',
            'scooter lost control', 'electric scooter crash fall',
            
            # Location-specific
            'sidewalk scooter accident', 'bike lane scooter accident', 'street scooter accident',
            'intersection scooter accident', 'scooter accident on road', 'parking lot scooter accident',
            
            # Scooter-specific issues
            'electric scooter malfunction', 'e-scooter brake failure', 'scooter battery fire',
            'scooter defect accident', 'electric scooter speed accident', 'scooter tire blowout',
            'scooter handlebar broke', 'electric scooter fell apart', 'scooter mechanical failure',
            
            # Fault indicators
            'driver fault scooter accident', 'negligent driver hit scooter', 'distracted driver hit scooter',
            'driver failed to see scooter', 'scooter right of way accident', 'unsafe scooter operation',
            
            # Company liability
            'lime scooter company liability', 'bird scooter company negligence', 'scooter company fault',
            'defective rental scooter', 'scooter sharing company liability', 'electric scooter recall',
            
            # Legal context
            'electric scooter accident lawyer', 'e-scooter accident attorney', 'scooter accident lawyer',
            'scooter accident claim', 'electric scooter accident settlement', 'scooter injury compensation',
            
            # Safety and helmet issues
            'scooter helmet accident', 'no helmet scooter accident', 'electric scooter safety',
            'scooter accident head injury', 'e-scooter concussion',
            
            # Severity indicators
            'serious scooter accident', 'severe electric scooter accident', 'fatal scooter accident',
            'catastrophic scooter injury'
        ],
        
        'atv_offroad_accidents': [
            # Core terms
            'atv accident', 'atv crash', 'atv wreck', 'atv collision', 'atv incident',
            'quad accident', 'quad crash', 'quad wreck', 'quad bike accident',
            '4-wheeler accident', '4 wheeler accident', 'four wheeler accident',
            'off-road vehicle accident', 'off road vehicle accident', 'offroad accident',
            
            # Intent-specific (injury context)
            'atv accident injury', 'atv injury', 'quad accident injury', 'atv accident victim',
            'injured on atv', 'hurt on quad', 'atv rider injured', 'quad rider injured',
            'atv personal injury', 'off-road accident injury',
            
            # Specific vehicle types
            'side by side accident', 'utv accident', 'utility vehicle accident', 'rzr accident',
            'polaris accident', 'can-am accident', 'honda atv accident', 'yamaha atv accident',
            'kawasaki atv accident', 'arctic cat accident',
            
            # Collision types
            'atv rollover', 'quad rollover', 'atv flip', 'atv rolled over', 'quad rolled over',
            'atv crash into tree', 'atv hit obstacle', 'atv vs car accident', 'car hit atv',
            'atv head on collision', 'atv rear ended', 'multiple atv accident',
            
            # ATV-specific issues
            'atv mechanical failure', 'atv brake failure', 'atv steering failure',
            'atv tire blowout', 'defective atv', 'atv recall accident', 'atv safety defect',
            'atv throttle stuck', 'atv lost control', 'inexperienced atv rider',
            
            # Fault and liability
            'atv manufacturer liability', 'defective atv lawsuit', 'atv dealer negligence',
            'atv rental company liability', 'unsafe atv conditions', 'atv guide negligence',
            'atv tour accident', 'commercial atv accident',
            
            # Safety equipment
            'atv helmet accident', 'no helmet atv accident', 'atv safety gear',
            'atv protective equipment', 'atv accident head injury',
            
            # Legal context
            'atv accident lawyer', 'atv accident attorney', 'off-road accident lawyer',
            'atv accident claim', 'atv accident settlement', 'atv injury compensation',
            'quad accident lawyer',
            
            # Severity indicators
            'serious atv accident', 'severe atv accident', 'fatal atv accident',
            'catastrophic atv accident', 'atv accident death',
            
            # Related activities
            'hunting atv accident', 'farming atv accident', 'recreational atv accident',
            'racing atv accident', 'mudding accident', 'atv racing crash'
        ],
        
        'parking_lot_accidents': [
            # Core terms
            'parking lot accident', 'parking lot crash', 'parking lot collision', 'parking lot wreck',
            'parking lot incident', 'car crash in parking lot', 'accident in parking lot',
            'parking garage accident', 'parking garage crash', 'parking structure accident',
            
            # Intent-specific (injury context)
            'parking lot accident injury', 'parking lot injury', 'injured in parking lot',
            'hurt in parking lot', 'parking lot accident victim', 'parking lot personal injury',
            
            # Pedestrian scenarios
            'parking lot pedestrian accident', 'parking lot pedestrian hit', 'pedestrian struck in parking lot',
            'hit by car in parking lot', 'parking lot pedestrian injury', 'walking in parking lot hit',
            'parking lot pedestrian vs car', 'shopping cart pedestrian accident',
            
            # Vehicle collision scenarios
            'parking lot fender bender', 'parking lot rear end', 'parking lot rear-end collision',
            'backing out accident', 'backing up accident parking lot', 'reversing accident parking lot',
            'parking lot side swipe', 'parking lot sideswipe', 'parking space accident',
            'pulling out of parking space accident', 'parking lot door ding accident',
            
            # Specific collision types
            'head on parking lot accident', 'parking lot t-bone accident', 'parking lot rollover',
            'parking lot hit and run', 'parking lot chain reaction accident',
            'shopping cart accident', 'runaway shopping cart injury',
            
            # Fault scenarios
            'parking lot right of way accident', 'parking lot yield accident', 'parking lot stop sign accident',
            'distracted driver parking lot', 'speeding in parking lot accident', 'texting while driving parking lot',
            'parking lot visibility accident', 'blind spot parking lot accident',
            
            # Property types
            'shopping center parking lot accident', 'mall parking lot accident', 'store parking lot accident',
            'grocery store parking lot accident', 'walmart parking lot accident', 'target parking lot accident',
            'restaurant parking lot accident', 'hospital parking lot accident', 'office parking lot accident',
            'apartment parking lot accident', 'school parking lot accident', 'church parking lot accident',
            
            # Structural issues
            'parking lot pothole accident', 'parking lot uneven surface', 'parking lot lighting accident',
            'poorly lit parking lot accident', 'parking lot design defect', 'parking lot maintenance negligence',
            'parking lot snow ice accident', 'slippery parking lot accident',
            
            # Legal context
            'parking lot accident lawyer', 'parking lot accident attorney', 'parking lot accident fault',
            'parking lot accident claim', 'parking lot accident settlement', 'who is at fault parking lot accident',
            'parking lot property owner liability', 'parking lot negligence',
            
            # Severity indicators
            'serious parking lot accident', 'severe parking lot injury', 'major parking lot accident',
            
            # Common phrases
            'parking lot accident no damage', 'parking lot accident minor', 'parking lot accident insurance',
            'parking lot private property accident'
        ],
        
        'boating_accidents': [
            # Core terms
            'boating accident', 'boat accident', 'boat crash', 'boat collision', 'boat wreck',
            'maritime accident', 'watercraft accident', 'vessel accident', 'marine accident',
            'boating incident', 'boat incident', 'watercraft incident',
            
            # Intent-specific (injury context)
            'boating accident injury', 'boat accident injury', 'injured on boat', 'hurt on boat',
            'boating accident victim', 'boat accident victim', 'marine injury', 'watercraft injury',
            'boating personal injury', 'boat passenger injured',
            
            # Vessel types
            'motorboat accident', 'speedboat accident', 'sailboat accident', 'yacht accident',
            'fishing boat accident', 'pontoon boat accident', 'cabin cruiser accident',
            'jet boat accident', 'bass boat accident', 'ski boat accident', 'pleasure craft accident',
            'commercial vessel accident', 'charter boat accident', 'ferry accident',
            'cruise ship accident', 'cruise ship injury', 'cruise line accident', 'passenger ship accident',
            
            # Collision types
            'boat vs boat collision', 'boat collision with dock', 'boat hit pier', 'boat grounding',
            'boat capsized', 'boat overturned', 'boat sinking', 'boat fire', 'boat explosion',
            'boat vs jetski collision', 'boat hit swimmer', 'boat propeller accident', 'propeller injury',
            
            # Water-specific scenarios
            'man overboard', 'fell off boat', 'thrown from boat', 'boat passenger overboard',
            'drowning from boat accident', 'boat rescue accident', 'water skiing accident behind boat',
            'tubing accident', 'wakeboarding accident', 'boat towing accident',
            
            # Fault scenarios
            'drunk boating accident', 'intoxicated boat operator', 'reckless boat operation',
            'speeding boat accident', 'negligent boat operator', 'inexperienced boat operator',
            'boat operator error', 'boating under influence', 'BUI accident',
            
            # Equipment and mechanical failures
            'boat engine failure', 'boat steering failure', 'boat brake failure', 'defective boat',
            'boat equipment failure', 'boat safety equipment failure', 'boat recall accident',
            'faulty boat motor', 'boat mechanical malfunction',
            
            # Safety equipment issues
            'no life jacket accident', 'life vest failure', 'boat safety violation',
            'missing safety equipment', 'inadequate safety equipment',
            
            # Legal context
            'boating accident lawyer', 'boat accident attorney', 'maritime lawyer',
            'boating accident claim', 'boat accident settlement', 'maritime law',
            'boating accident compensation', 'vessel liability',
            
            # Liability scenarios
            'boat owner liability', 'boat operator liability', 'boat rental company negligence',
            'marina negligence', 'boat dealer liability', 'boat manufacturer liability',
            'charter company negligence', 'cruise ship negligence', 'cruise line liability',
            'cruise ship medical malpractice', 'cruise ship slip and fall', 'cruise ship food poisoning',
            
            # Severity indicators
            'serious boating accident', 'severe boat accident', 'fatal boating accident',
            'catastrophic boating accident', 'major marine accident',
            
            # Coast Guard and regulations
            'coast guard boating accident', 'boating safety violation', 'maritime regulation violation',
            'boating accident report', 'vessel accident investigation'
        ],
        
        'aviation_accidents': [
            # Core terms
            'aviation accident', 'aircraft accident', 'plane accident', 'airplane accident', 'plane crash',
            'aircraft crash', 'airplane crash', 'aviation crash', 'aviation incident', 'aircraft incident',
            'flight accident', 'air accident', 'aeronautical accident',
            
            # Helicopter terms
            'helicopter accident', 'helicopter crash', 'helicopter wreck', 'chopper accident',
            'chopper crash', 'rotorcraft accident', 'helicopter incident',
            
            # Intent-specific (injury context)
            'aviation accident injury', 'plane accident injury', 'aircraft accident injury',
            'injured in plane crash', 'hurt in aviation accident', 'aviation accident victim',
            'aircraft accident victim', 'plane crash victim', 'aviation personal injury',
            'helicopter accident injury', 'helicopter crash victim',
            
            # Aircraft types
            'commercial airplane accident', 'commercial aviation accident', 'airline accident',
            'private plane accident', 'private aircraft accident', 'charter flight accident',
            'corporate jet accident', 'business jet accident', 'small plane accident',
            'light aircraft accident', 'single engine plane accident', 'twin engine plane accident',
            
            # Helicopter types
            'medical helicopter accident', 'life flight accident', 'air ambulance accident',
            'news helicopter accident', 'police helicopter accident', 'tour helicopter accident',
            'sightseeing helicopter accident', 'helicopter tour accident',
            
            # Phase of flight
            'takeoff accident', 'landing accident', 'runway accident', 'airport accident',
            'in-flight accident', 'taxiing accident', 'ground accident aviation',
            'emergency landing accident', 'forced landing accident',
            
            # Collision types
            'mid-air collision', 'aircraft collision', 'plane vs helicopter collision',
            'runway collision', 'ground collision aviation', 'bird strike accident',
            'aircraft vs vehicle collision', 'plane hit building',
            
            # Equipment and mechanical failures
            'aircraft engine failure', 'plane engine failure', 'helicopter engine failure',
            'aircraft mechanical failure', 'defective aircraft', 'aircraft recall',
            'aviation equipment failure', 'aircraft maintenance failure', 'faulty aircraft part',
            
            # Weather-related
            'aviation weather accident', 'plane crash weather', 'helicopter weather accident',
            'turbulence injury', 'severe turbulence accident', 'wind shear accident',
            
            # Pilot error and human factors
            'pilot error accident', 'aviation human error', 'pilot negligence',
            'air traffic control error', 'aviation communication failure',
            'pilot fatigue accident', 'aviation crew error',
            
            # Legal context
            'aviation accident lawyer', 'aviation lawyer', 'plane crash attorney',
            'aircraft accident attorney', 'helicopter accident lawyer', 'aviation law',
            'aviation accident claim', 'aircraft accident settlement', 'aviation litigation',
            
            # Liability scenarios
            'airline liability', 'aircraft manufacturer liability', 'pilot liability',
            'aviation company negligence', 'aircraft maintenance negligence', 'airport negligence',
            'air traffic control negligence', 'helicopter company liability',
            
            # Severity indicators
            'serious aviation accident', 'severe aircraft accident', 'fatal plane crash',
            'catastrophic aviation accident', 'major aircraft accident', 'devastating plane crash',
            
            # Investigation and regulatory
            'NTSB aviation accident', 'FAA aviation accident', 'aircraft accident investigation',
            'aviation safety violation', 'aircraft certification failure'
        ],
        
        'railroad_accidents': [
            # Core terms - REMOVED standalone "train"
            'railroad accident', 'railway accident', 'rail accident', 'locomotive accident',
            'railcar accident', 'freight train accident', 'passenger train accident', 'train collision',
            'train crash', 'train wreck', 'train incident',
            
            # Intent-specific (injury context)
            'railroad accident injury', 'railway accident injury', 'injured by train', 'hurt by train',
            'train accident victim', 'railroad accident victim', 'train personal injury',
            'struck by train', 'hit by train', 'train vs person accident',
            
            # Train types
            'freight train accident', 'cargo train accident', 'passenger train accident',
            'commuter train accident', 'amtrak accident',
            
            # Collision types
            'train derailment', 'train derailed', 'railroad derailment', 'train off tracks',
            'train vs car accident', 'train vs truck accident', 'train vs vehicle collision',
            'train vs train collision', 'head on train collision', 'train rear end collision',
            'railroad crossing accident', 'grade crossing accident', 'level crossing accident',
            
            # Location-specific accidents
            'railroad station accident', 'train platform accident',
            'train boarding accident', 'train yard accident',
            'railroad yard accident', 'train maintenance facility accident',
            
            # Pedestrian scenarios
            'pedestrian train accident', 'pedestrian struck by train', 'trespasser train accident',
            'railroad trespassing accident', 'walking on tracks accident', 'train vs pedestrian',
            
            # Equipment and mechanical failures
            'train brake failure', 'locomotive failure', 'train mechanical failure',
            'railroad equipment failure', 'defective train', 'train signal failure',
            'railroad signal malfunction', 'crossing gate failure', 'railroad crossing malfunction',
            
            # Human error factors
            'train operator error', 'railroad crew negligence', 'train conductor error',
            'railroad dispatcher error', 'train speed violation', 'train safety violation',
            
            # Specific scenarios
            'fell between train cars', 'train door accident',
            'train electrical accident', 'third rail accident', 'overhead wire accident',
            'train fire accident', 'train explosion', 'hazardous material train accident',
            
            # Legal context
            'railroad accident lawyer', 'railroad accident attorney', 'train accident attorney',
            'railway accident lawyer', 'train accident claim', 'railroad accident settlement',
            'train accident compensation', 'railroad injury law', 'FELA claim',
            
            # Liability scenarios
            'railroad company negligence', 'train company liability', 'railroad negligence',
            'train operator liability', 'railroad crossing negligence', 'amtrak negligence',
            'railroad maintenance negligence',
            
            # Severity indicators
            'serious train accident', 'severe railroad accident', 'fatal train accident',
            'catastrophic train accident', 'major train derailment', 'devastating train crash',
            
            # Investigation and regulatory
            'FRA railroad accident', 'railroad accident investigation', 'train safety investigation',
            'railroad safety violation', 'train accident report'
        ],
        
        'public_transportation': [
            # Core terms
            'bus accident', 'bus crash', 'bus wreck', 'bus collision', 'bus incident',
            'transit accident', 'public transit accident', 'public transit injury', 'transit injury',
            'public transportation accident', 'mass transit accident',
            
            # Bus types
            'city bus accident', 'municipal bus accident', 'transit bus accident', 'public bus accident',
            'school bus accident', 'charter bus accident', 'tour bus accident', 'intercity bus accident',
            'commuter bus accident', 'shuttle bus accident', 'commercial bus accident',
            'greyhound bus accident', 'megabus accident',
            
            # Rail transit - SEPARATED from railroad accidents
            'subway accident', 'metro accident', 'light rail accident', 'streetcar accident',
            'trolley accident', 'rapid transit accident', 'subway train accident',
            'underground accident', 'tube accident', 'rail transit accident',
            
            # Intent-specific (injury context)
            'bus accident injury', 'transit accident injury', 'injured on bus', 'hurt on bus',
            'bus accident victim', 'transit accident victim', 'bus passenger injured',
            'subway accident injury', 'metro accident injury', 'injured on subway',
            
            # Collision scenarios
            'bus vs car accident', 'bus hit car', 'car hit bus', 'bus rear ended',
            'bus sideswiped', 'bus rollover', 'bus vs truck collision', 'bus head on collision',
            'subway collision', 'metro collision',
            
            # Boarding and platform accidents
            'bus boarding accident', 'bus door accident', 'bus slip and fall',
            'subway platform accident', 'metro platform accident', 'fell on subway tracks',
            'subway door accident', 'metro door accident', 'transit platform injury',
            'bus stop accident', 'waiting for bus accident',
            
            # Bus-specific scenarios
            'bus sudden stop injury', 'bus sharp turn injury', 'standing on bus injury',
            'bus aisle injury', 'bus wheelchair accident', 'bus accessibility accident',
            'school bus stop accident', 'getting off bus accident', 'getting on bus accident',
            
            # Equipment failures
            'bus brake failure', 'bus mechanical failure', 'subway brake failure',
            'transit vehicle malfunction', 'bus door malfunction', 'subway signal failure',
            'defective bus', 'defective transit vehicle',
            
            # Driver/operator factors
            'bus driver negligence', 'bus driver error', 'transit operator negligence',
            'bus driver distracted', 'reckless bus driving', 'speeding bus accident',
            'subway operator error', 'metro operator negligence',
            
            # Legal context
            'bus accident lawyer', 'transit accident attorney', 'public transportation lawyer',
            'bus accident attorney', 'subway accident lawyer', 'metro accident attorney',
            'bus accident claim', 'transit accident settlement', 'public transit compensation',
            
            # Liability scenarios
            'transit authority negligence', 'bus company negligence', 'municipal bus negligence',
            'school district bus negligence', 'charter bus company liability', 'tour bus negligence',
            'subway authority liability', 'metro authority negligence', 'transit operator liability',
            
            # Severity indicators
            'serious bus accident', 'severe transit accident', 'major bus crash',
            'fatal bus accident', 'catastrophic transit accident',
            
            # Common phrases
            'bus accident fault', 'public transit safety', 'transit accident investigation',
            'bus passenger rights', 'public transportation injury'
        ],
        
        'drunk_driving': [
            # Core terms
            'drunk driving accident', 'drunk driver accident', 'dui accident', 'dwi accident',
            'intoxicated driver accident', 'impaired driver accident', 'drunk driving crash',
            'drunk driver crash', 'alcohol related accident', 'drinking and driving accident',
            
            # Victim perspective
            'injured by drunk driver', 'hit by drunk driver', 'hurt by drunk driver',
            'drunk driving victim', 'drunk driver hit me', 'struck by drunk driver',
            'drunk driving accident victim', 'innocent victim drunk driver',
            
            # Legal terms
            'driving under influence accident', 'DUI crash', 'DWI crash', 'OUI accident',
            'drunk driving personal injury', 'drunk driving claim', 'drunk driving lawsuit',
            'drunk driving settlement', 'drunk driving compensation',
            
            # Fault and liability
            'drunk driver fault', 'intoxicated driver liability', 'drunk driver negligence',
            'bar liability drunk driving', 'dram shop liability', 'social host liability',
            'over serving liability', 'liquor store liability',
            
            # Severity indicators
            'serious drunk driving accident', 'fatal drunk driving accident', 'catastrophic drunk driving accident',
            'deadly drunk driving crash', 'severe drunk driving injury',
            
            # Legal context
            'drunk driving accident lawyer', 'drunk driving accident attorney', 'dui accident lawyer',
            'drunk driving victim lawyer', 'drunk driving injury attorney',
            
            # Related scenarios
            'repeat drunk driver accident', 'underage drunk driving accident', 'drunk driving hit and run',
            'drunk driving wrong way accident', 'drunk driving head on collision',
            
            # Common phrases
            'drunk driving accident statistics', 'drunk driving accident prevention',
            'drunk driving accident lawsuit', 'drunk driving accident insurance claim'
        ],
    },

    # 2. Premises Liability
    'premises_liability': {
        'premise_liability': [
            # Core terms - REMOVED specific property types that have their own categories
            'premise liability', 'premises liability', 'property liability', 'dangerous property',
            'hazardous property', 'unsafe premises', 'unsafe conditions', 'dangerous conditions',
            'property negligence', 'landowner negligence', 'property owner negligence',
            
            # Generic commercial property
            'commercial property accident', 'business property injury', 'office building accident',
            'shopping center accident', 'mall accident', 'strip mall accident',
            
            # Generic residential property
            'apartment complex accident', 'condo accident', 'rental property accident',
            'landlord negligence', 'tenant injury', 'apartment building accident',
            
            # Property conditions
            'inadequate lighting accident', 'poor lighting injury', 'inadequate security injury',
            'property maintenance negligence', 'building maintenance accident', 'property defect injury',
            
            # Legal context
            'premise liability lawyer', 'property accident attorney', 'premise liability claim',
            'property owner liability', 'landowner liability', 'premise liability settlement'
        ],
        
        'slip_trip_fall': [
            # Core terms - REMOVED standalone "slip" and "fall" 
            'slip and fall', 'slip and fall accident', 'slip and fall injury', 'trip and fall',
            'trip and fall accident', 'fall injury', 'fall accident', 'falling accident',
            'slipped and fell', 'tripped and fell', 'fell down', 'accidental fall',
            
            # Causes
            'wet floor slip', 'wet floor fall', 'slippery floor accident', 'spilled liquid fall',
            'uneven surface fall', 'cracked pavement fall', 'broken sidewalk fall',
            'loose carpet fall', 'torn carpet trip', 'wrinkled rug fall',
            'debris on floor fall', 'object on floor trip', 'merchandise on floor fall',
            
            # Locations
            'store slip and fall', 'restaurant slip and fall', 'hotel slip and fall',
            'hospital slip and fall', 'office slip and fall', 'mall slip and fall',
            'grocery store slip and fall', 'walmart slip and fall', 'target slip and fall',
            'sidewalk slip and fall', 'parking lot slip and fall', 'stairway fall',
            
            # Stair-related
            'stair fall', 'stairway accident', 'stairs accident', 'fell down stairs',
            'broken stair fall', 'missing handrail fall', 'defective stairs fall',
            'staircase accident', 'step accident', 'escalator fall',
            
            # Weather-related
            'ice slip and fall', 'snow slip and fall', 'icy sidewalk fall', 'winter slip and fall',
            'rain slip and fall', 'wet pavement fall', 'slippery conditions fall',
            
            # Legal context
            'slip and fall lawyer', 'slip and fall attorney', 'trip and fall lawyer',
            'fall accident attorney', 'slip and fall claim', 'slip and fall settlement',
            'slip and fall compensation', 'fall injury lawsuit',
            
            # Severity
            'serious slip and fall', 'severe fall injury', 'slip and fall head injury',
            'slip and fall broken bone', 'slip and fall back injury', 'slip and fall hip fracture'
        ],
        
        'store_retail_accidents': [
            # Store and retail - MOVED from premises liability to avoid duplication
            'store accident', 'retail store accident', 'shopping injury', 'merchandise falling',
            'store negligence', 'retail negligence', 'grocery store accident', 'supermarket accident',
            'department store accident', 'walmart accident', 'target accident', 'costco accident',
            'store slip and fall', 'retail slip and fall', 'shopping cart accident',
            'store merchandise injury', 'falling merchandise', 'store aisle accident',
            'store display accident', 'retail fixture accident', 'store equipment accident',
            'grocery store injury', 'supermarket injury', 'department store injury',
            'big box store accident', 'chain store accident', 'retail chain accident',
            
            # Legal context
            'store accident lawyer', 'retail negligence attorney', 'store injury claim',
            'retail accident settlement', 'store liability lawsuit', 'merchant liability'
        ],
        
        'restaurant_bar_accidents': [
            # Restaurant and bar liability - MOVED from premises liability
            'restaurant liability', 'restaurant negligence', 'bar negligence', 'tavern liability',
            'dram shop', 'dram shop liability', 'over serving alcohol', 'bar fight injury',
            'restaurant accident', 'cafe accident', 'fast food restaurant accident',
            'restaurant slip and fall', 'bar slip and fall', 'tavern accident',
            'restaurant food poisoning', 'restaurant burn injury', 'hot food burns',
            'spilled hot coffee', 'hot oil burns', 'restaurant kitchen accident',
            'server accident', 'waiter spilled hot food', 'waitress accident',
            'restaurant staff negligence', 'bar staff negligence', 'bartender negligence',
            
            # Legal context
            'restaurant accident lawyer', 'bar negligence attorney', 'dram shop lawyer',
            'restaurant liability claim', 'bar accident settlement'
        ],
        
        'amusement_park_injuries': [
            # Core terms
            'amusement park accident', 'amusement park injury', 'theme park accident', 'theme park injury',
            'carnival accident', 'carnival injury', 'fair accident', 'fair injury',
            'water park accident', 'water park injury', 'waterpark accident', 'waterpark injury',
            
            # Ride-specific
            'roller coaster accident', 'roller coaster injury', 'ferris wheel accident',
            'bumper car accident', 'merry go round accident', 'carousel accident',
            'log flume accident', 'water slide accident', 'lazy river accident',
            'wave pool accident', 'kiddie ride accident', 'spinning ride accident',
            
            # Major theme parks
            'disney accident', 'disneyland accident', 'disney world accident', 'universal studios accident',
            'six flags accident', 'busch gardens accident', 'cedar point accident',
            'knott berry farm accident', 'seaworld accident',
            
            # Incident types
            'ride malfunction', 'mechanical failure ride', 'ride operator error', 'ride safety failure',
            'fell from ride', 'thrown from ride', 'ride restraint failure', 'safety harness failure',
            'ride collision', 'ride derailment', 'ride stopped suddenly',
            
            # Water park specific
            'water slide injury', 'pool accident', 'diving accident', 'splash pad accident',
            'tube accident', 'raft accident', 'water attraction injury',
            
            # Legal context
            'amusement park accident lawyer', 'theme park injury attorney', 'ride accident lawyer',
            'amusement park negligence', 'theme park liability', 'ride manufacturer liability',
            'amusement park injury claim', 'theme park accident settlement'
        ],
        
        'dog_bites': [
            # Core terms
            'dog bite', 'dog attack', 'dog bite injury', 'dog attack injury', 'bitten by dog',
            'dog mauling', 'canine attack', 'animal attack', 'pet attack', 'vicious dog attack',
            
            # Animal types
            'pit bull attack', 'german shepherd attack', 'rottweiler attack', 'doberman attack',
            'large dog attack', 'aggressive dog bite', 'stray dog attack', 'neighbor dog bite',
            'family dog bite', 'puppy bite', 'rescue dog attack',
            
            # Victim types
            'child dog bite', 'toddler dog attack', 'elderly dog bite', 'postal worker dog bite',
            'delivery driver dog bite', 'jogger dog attack', 'walker dog bite',
            
            # Locations
            'dog bite on property', 'dog bite at home', 'dog bite in yard', 'dog bite at park',
            'dog bite on sidewalk', 'dog bite while walking', 'dog bite trespassing',
            
            # Severity
            'serious dog bite', 'severe dog attack', 'dog bite requiring surgery', 'dog bite scarring',
            'dog bite infection', 'rabies exposure', 'dog bite nerve damage', 'dog bite amputation',
            
            # Legal terms
            'dog bite liability', 'dog owner liability', 'strict liability dog bite', 'one bite rule',
            'dangerous dog statute', 'vicious dog law', 'dog bite statute',
            
            # Legal context
            'dog bite lawyer', 'dog attack attorney', 'dog bite attorney', 'animal attack lawyer',
            'dog bite claim', 'dog bite settlement', 'dog bite compensation', 'dog bite lawsuit',
            
            # Related scenarios
            'dog bite while working', 'dog bite on job', 'unleashed dog attack', 'off leash dog bite',
            'dog bite provocation', 'unprovoked dog attack', 'dog bite history', 'repeat dog bite'
        ],
        
        'elevator_escalator_injury': [
            # Elevator accidents
            'elevator accident', 'elevator injury', 'elevator malfunction', 'elevator failure',
            'stuck in elevator', 'elevator drop', 'elevator fall', 'elevator plunge',
            'elevator door accident', 'elevator door injury', 'crushed by elevator door',
            'elevator entrapment', 'elevator shaft accident', 'elevator cable break',
            
            # Escalator accidents
            'escalator accident', 'escalator injury', 'escalator malfunction', 'escalator entrapment',
            'escalator fall', 'fell on escalator', 'escalator step collapse', 'escalator clothing caught',
            'escalator shoe caught', 'escalator hand injury', 'escalator finger injury',
            'escalator side panel accident', 'escalator comb plate injury',
            
            # Locations
            'mall elevator accident', 'office building elevator accident', 'hospital elevator accident',
            'apartment elevator accident', 'hotel elevator accident', 'parking garage elevator accident',
            'mall escalator accident', 'airport escalator accident', 'subway escalator accident',
            
            # Legal context
            'elevator accident lawyer', 'escalator injury attorney', 'elevator malfunction lawsuit',
            'elevator company negligence', 'escalator manufacturer liability', 'building owner liability',
            'elevator maintenance negligence', 'escalator accident claim', 'elevator injury settlement'
        ],
        
        'drowning_accidents': [
            # Core terms
            'drowning accident', 'near drowning', 'swimming pool accident', 'pool accident',
            'pool drowning', 'swimming accident', 'water accident', 'aquatic accident',
            
            # Pool types
            'residential pool accident', 'backyard pool drowning', 'private pool accident',
            'public pool accident', 'community pool accident', 'hotel pool accident',
            'apartment pool accident', 'condo pool accident', 'school pool accident',
            
            # Victim types
            'child drowning', 'toddler drowning', 'infant drowning', 'adult drowning',
            'non-swimmer drowning', 'weak swimmer accident', 'guest drowning',
            
            # Causes
            'lack of supervision drowning', 'inadequate lifeguarding', 'missing pool fence',
            'defective pool gate', 'pool drain entrapment', 'suction entrapment',
            'pool equipment failure', 'diving accident', 'shallow water diving',
            
            # Pool safety
            'pool fence violation', 'missing pool alarm', 'inadequate pool barriers',
            'pool safety violation', 'swimming pool negligence', 'pool owner negligence',
            
            # Legal context
            'drowning accident lawyer', 'pool accident attorney', 'swimming pool liability',
            'pool owner liability', 'drowning wrongful death', 'pool accident settlement',
            'swimming pool insurance claim', 'pool negligence lawsuit'
        ],
        
        'food_poisoning': [
            # Core terms
            'food poisoning', 'foodborne illness', 'food contamination', 'contaminated food',
            'food safety violation', 'restaurant food poisoning', 'catering food poisoning',
            
            # Specific pathogens
            'salmonella poisoning', 'e coli poisoning', 'listeria poisoning', 'norovirus food poisoning',
            'campylobacter poisoning', 'botulism poisoning', 'hepatitis a food poisoning',
            
            # Food types
            'seafood poisoning', 'chicken food poisoning', 'beef food poisoning', 'dairy food poisoning',
            'produce contamination', 'lettuce contamination', 'spinach contamination',
            
            # Locations
            'restaurant food poisoning', 'fast food poisoning', 'catering food poisoning',
            'wedding food poisoning', 'school food poisoning', 'nursing home food poisoning',
            'hospital food poisoning', 'cruise ship food poisoning',
            
            # Legal context
            'food poisoning lawyer', 'foodborne illness attorney', 'food contamination lawsuit',
            'restaurant negligence food poisoning', 'food poisoning settlement', 'food safety lawsuit',
            'food poisoning compensation', 'foodborne illness claim'
        ],
        
        'hotel_injuries': [
            # Core terms
            'hotel accident', 'hotel injury', 'motel accident', 'motel injury', 'inn accident',
            'resort accident', 'resort injury', 'bed and breakfast accident',
            
            # Hotel-specific accidents
            'hotel slip and fall', 'hotel bathroom accident', 'hotel balcony accident',
            'hotel pool accident', 'hotel elevator accident', 'hotel stair accident',
            'hotel room accident', 'hotel lobby accident', 'hotel parking lot accident',
            
            # Security issues
            'hotel crime', 'hotel assault', 'hotel robbery', 'inadequate hotel security',
            'hotel negligent security', 'hotel room break in', 'hotel guest attack',
            
            # Safety issues
            'hotel fire', 'hotel carbon monoxide', 'hotel gas leak', 'hotel electrical accident',
            'hotel bed bug infestation', 'hotel mold exposure', 'hotel water damage',
            
            # Legal context
            'hotel negligence', 'hotel liability', 'innkeeper liability', 'hotel accident lawyer',
            'hotel injury attorney', 'hotel accident claim', 'hotel negligence lawsuit',
            'hotel accident settlement', 'resort accident attorney'
        ],
        
        'negligent_security': [
            # Core terms
            'negligent security', 'inadequate security', 'lack of security', 'poor security',
            'insufficient security', 'security negligence', 'property security failure',
            
            # Criminal acts on property
            'assault on property', 'attack on property', 'robbery on property', 'mugging on property',
            'rape on property', 'sexual assault on property', 'shooting on property',
            'stabbing on property', 'violence on property', 'crime victim on property',
            
            # Security measures
            'no security cameras', 'broken security cameras', 'inadequate lighting',
            'poor lighting crime', 'no security guard', 'untrained security', 'defective locks',
            'broken gate security', 'inadequate access control',
            
            # Property types
            'apartment complex crime', 'parking lot crime', 'mall crime', 'hotel crime',
            'bar crime', 'nightclub crime', 'gas station crime', 'convenience store crime',
            'shopping center crime', 'office building crime',
            
            # Legal context
            'negligent security lawyer', 'inadequate security attorney', 'property crime lawsuit',
            'security negligence claim', 'inadequate security settlement', 'property owner liability crime',
            'landlord security negligence', 'business security negligence'
        ],
        
        'snow_ice_accidents': [
            # Core terms
            'snow slip and fall', 'ice slip and fall', 'winter slip and fall', 'icy slip and fall',
            'slippery conditions fall', 'winter weather accident', 'snow and ice injury',
            
            # Specific conditions
            'icy sidewalk fall', 'icy parking lot fall', 'icy steps fall', 'icy walkway fall',
            'snow covered walkway fall', 'slush slip and fall', 'black ice fall',
            'frozen precipitation fall', 'winter storm accident',
            
            # Property maintenance
            'failure to remove snow', 'failure to salt walkway', 'inadequate snow removal',
            'poor ice treatment', 'negligent snow removal', 'untimely snow clearing',
            
            # Locations
            'sidewalk ice fall', 'driveway ice fall', 'entrance ice fall', 'store entrance ice fall',
            'restaurant ice fall', 'office building ice fall', 'mall ice fall',
            
            # Legal context
            'snow removal negligence', 'ice accident lawyer', 'winter slip and fall attorney',
            'snow and ice liability', 'property owner snow liability', 'commercial snow removal negligence'
        ],
        
        'structural_failures': [
            # Building collapses
            'building collapse', 'structure collapse', 'wall collapse', 'roof collapse',
            'ceiling collapse', 'floor collapse', 'partial building collapse', 'total building collapse',
            
            # Specific structures
            'deck collapse', 'balcony collapse', 'porch collapse', 'stair collapse',
            'railing collapse', 'handrail failure', 'bridge collapse', 'walkway collapse',
            'canopy collapse', 'awning collapse', 'scaffolding collapse',
            
            # Falling objects
            'falling debris', 'falling object injury', 'falling construction material',
            'falling facade', 'falling brick', 'falling concrete', 'falling glass',
            'falling ice', 'falling tree branch', 'falling sign',
            
            # Construction defects
            'construction defect', 'faulty construction', 'building code violation',
            'structural engineering failure', 'foundation failure', 'design defect',
            'material failure', 'construction negligence',
            
            # Legal context
            'structural failure lawyer', 'building collapse attorney', 'construction defect lawyer',
            'architect negligence', 'engineer negligence', 'contractor negligence',
            'building owner liability', 'structural failure lawsuit'
        ],
    },

    # 3. Child Injuries
    'child_injuries': {
        'general_child_injuries': [
            # Core terms
            'child injury', 'child accident', 'injured child', 'hurt child', 'pediatric injury',
            'child injury victim', 'injured minor', 'minor injured', 'child trauma',
            'child personal injury', 'juvenile injury',
            
            # Age-specific
            'toddler injury', 'infant injury', 'baby injury', 'preschooler injury',
            'elementary school child injury', 'middle school child injury', 'teenager injury',
            'teen injury', 'adolescent injury',
            
            # Legal context
            'child injury lawyer', 'pediatric injury attorney', 'minor injury claim',
            'child accident settlement', 'child injury compensation', 'minor injury lawsuit',
            'guardian ad litem', 'child injury court approval'
        ],
        
        'school_playground_injuries': [
            # School accidents
            'school injury', 'school accident', 'injured at school', 'hurt at school',
            'school negligence', 'school liability', 'public school accident', 'private school accident',
            'elementary school accident', 'middle school accident', 'high school accident',
            
            # Playground accidents
            'playground accident', 'playground injury', 'playground equipment accident',
            'swing accident', 'slide accident', 'monkey bars accident', 'seesaw accident',
            'jungle gym accident', 'playground fall', 'playground equipment failure',
            
            # Campus areas
            'campus injury', 'school hallway accident', 'school cafeteria accident',
            'school bathroom accident', 'school gymnasium accident',
            'school field accident', 'school parking lot accident',
            
            # School-specific issues
            'defective playground equipment', 'inadequate playground supervision',
            'playground surface injury', 'playground maintenance negligence',
            'school supervision negligence', 'teacher negligence', 'school staff negligence',
            
            # Legal context
            'school accident lawyer', 'school injury attorney', 'school negligence lawsuit',
            'playground accident lawyer', 'school district liability', 'educational negligence',
            'school accident claim', 'playground injury settlement'
        ],
        
        'childcare_facility_injuries': [
            # Daycare accidents
            'daycare injury', 'daycare accident', 'injured at daycare', 'hurt at daycare',
            'daycare negligence', 'daycare liability', 'daycare supervision negligence',
            'daycare abuse', 'daycare staff abuse', 'daycare worker abuse',
            
            # Childcare facilities
            'childcare injury', 'childcare accident', 'childcare negligence', 'childcare abuse',
            'childcare facility accident', 'childcare center injury', 'preschool injury',
            'nursery school accident', 'child development center injury',
            
            # Specific scenarios
            'daycare fall accident', 'daycare playground accident', 'daycare choking incident',
            'daycare food allergy reaction', 'daycare medication error', 'daycare burn injury',
            'daycare head injury', 'inadequate daycare supervision', 'daycare equipment accident',
            
            # Legal context
            'daycare accident lawyer', 'childcare negligence attorney', 'daycare abuse lawyer',
            'childcare facility liability', 'daycare licensing violation', 'daycare insurance claim'
        ],
        
        'child_abuse_and_neglect': [
            # Physical abuse
            'child abuse', 'child physical abuse', 'child beating', 'child assault',
            'child battery', 'child violence', 'abused child', 'battered child',
            
            # Neglect
            'child neglect', 'child abandonment', 'failure to supervise child',
            'inadequate child supervision', 'child endangerment', 'neglected child',
            
            # Sexual abuse
            'child sexual abuse', 'child molestation', 'child sexual assault',
            'sexual abuse of minor', 'child predator', 'pedophile abuse',
            
            # Institutional abuse
            'foster care abuse', 'residential facility abuse', 'group home abuse',
            'juvenile detention abuse', 'institutional child abuse',
            
            # Legal context
            'child abuse lawyer', 'child abuse attorney', 'child protection lawsuit',
            'child abuse compensation', 'mandatory reporter negligence', 'CPS negligence'
        ],
        
        'hazing_injuries': [
            # Core terms
            'hazing injury', 'hazing accident', 'hazing incident', 'hazing assault',
            'hazing abuse', 'ritual hazing', 'initiation injury', 'initiation accident',
            
            # Greek life
            'fraternity injury', 'sorority injury', 'fraternity hazing', 'sorority hazing',
            'greek life injury', 'pledge injury', 'fraternity assault', 'sorority assault',
            'fraternity alcohol poisoning', 'fraternity death', 'sorority death',
            
            # Sports hazing
            'athletic hazing', 'sports team hazing', 'locker room hazing',
            'team initiation injury', 'coach hazing', 'sports hazing injury',
            
            # Other organizations
            'band hazing', 'military hazing', 'club hazing', 'organization hazing',
            'student group hazing', 'academic hazing',
            
            # Legal context
            'hazing lawsuit', 'hazing liability', 'anti-hazing law violation',
            'fraternity negligence', 'university hazing liability', 'hazing injury lawyer'
        ],
        
        'child_sports_injuries': [
            # Core terms - REMOVED generic "sports injury" to avoid overlap with adult category
            'child sports injury', 'youth sports injury', 'minor sports injury', 
            'juvenile sports accident', 'student athlete injury', 'kids sports accident',
            
            # Specific sports
            'youth football injury', 'little league injury', 'soccer child injury',
            'basketball child injury', 'baseball child injury', 'hockey child injury',
            'gymnastics child injury', 'wrestling child injury', 'track child injury',
            
            # Injury types
            'child concussion sports', 'youth head injury sports', 'child broken bone sports',
            'growth plate injury', 'overuse injury child', 'heat exhaustion child sports',
            
            # Coaching and supervision
            'coach negligence child', 'inadequate sports supervision', 'unsafe sports conditions',
            'defective sports equipment child', 'sports facility negligence child',
            
            # Legal context
            'youth sports injury lawyer', 'child sports accident attorney',
            'sports negligence child', 'athletic liability child', 'sports injury settlement child'
        ],
    },

    # 4. Product & Medical Device Liability
    'product_medical_device_liability': {
        'defective_products': [
            # Core terms - REMOVED standalone "accident"
            'product liability', 'defective product', 'dangerous product', 'product defect',
            'faulty product', 'unsafe product', 'product failure', 'product malfunction',
            'product recall', 'recalled product', 'defective design', 'manufacturing defect',
            
            # Consumer products
            'defective appliance', 'defective toy', 'dangerous toy', 'toy recall',
            'defective electronics', 'defective furniture', 'defective tool',
            'power tool accident', 'lawn mower accident', 'chainsaw accident',
            
            # Legal context
            'product liability lawyer', 'defective product attorney', 'product recall lawsuit',
            'manufacturer liability', 'product liability claim', 'defective product settlement',
            'strict liability product', 'negligent design', 'failure to warn'
        ],
        
        'no_warning_labels': [
            # Warning label issues
            'missing warning label', 'inadequate warning label', 'unclear warning label',
            'insufficient warning', 'failure to warn', 'inadequate instructions',
            'unclear product warnings', 'missing safety instructions', 'defective labeling',
            
            # Specific contexts
            'prescription drug warning', 'chemical product warning', 'tool safety warning',
            'appliance warning missing', 'toy age warning missing', 'choking hazard warning',
            
            # Legal context
            'failure to warn lawsuit', 'inadequate warning claim', 'labeling negligence',
            'warning label attorney', 'product instruction negligence'
        ],
        
        'harmful_medications': [
            # Core terms - REMOVED standalone "drug"
            'defective drug', 'dangerous drug', 'harmful medication', 'pharmaceutical liability',
            'prescription drug injury', 'medication injury', 'medication side effects', 
            'adverse drug reaction', 'prescription drug recall', 'medication recall',
            
            # Specific issues
            'prescription side effects', 'over the counter drug injury', 'generic drug defect',
            'drug manufacturing defect', 'contaminated medication', 'wrong medication',
            'medication overdose', 'drug interaction injury', 'allergic reaction medication',
            
            # Legal context
            'pharmaceutical lawsuit', 'prescription drug injury lawyer', 'medication injury attorney',
            'prescription drug lawyer', 'pharmaceutical negligence', 'drug company liability',
            'medication error lawsuit', 'pharmacy negligence'
        ],
        
        'faulty_medical_devices': [
            # Core terms
            'defective medical device', 'faulty medical device', 'medical device failure',
            'medical device malfunction', 'medical device recall', 'dangerous medical device',
            'medical device defect', 'implant failure', 'medical implant defect',
            
            # Specific devices
            'pacemaker defect', 'hip implant failure', 'knee implant defect', 'surgical mesh',
            'stent failure', 'catheter defect', 'insulin pump malfunction', 'defibrillator defect',
            'prosthetic defect', 'surgical instrument defect', 'ventilator malfunction',
            
            # Legal context
            'medical device lawsuit', 'medical device attorney', 'implant failure lawyer',
            'medical device manufacturer liability', 'FDA medical device recall',
            'medical device injury claim', 'implant defect settlement'
        ],
        
        'auto_defects': [
            # Core terms
            'defective vehicle', 'car defect', 'auto defect', 'vehicle malfunction',
            'auto recall', 'car recall', 'vehicle recall', 'automotive defect',
            'manufacturing defect vehicle', 'design defect vehicle',
            
            # Specific defects
            'brake defect', 'accelerator defect', 'steering defect', 'airbag defect',
            'seatbelt defect', 'engine defect', 'transmission defect', 'fuel system defect',
            'electrical system defect', 'suspension defect', 'door latch defect',
            
            # Legal context
            'auto defect lawyer', 'vehicle defect attorney', 'car manufacturer liability',
            'automotive lawsuit', 'lemon law', 'auto defect settlement',
            'vehicle recall lawsuit', 'car defect claim'
        ],
        
        'tire_defects': [
            # Core terms
            'tire blowout', 'defective tire', 'tire failure', 'tire defect',
            'tire separation', 'tire recall', 'faulty tire', 'tire tread separation',
            
            # Specific issues
            'tire manufacturing defect', 'tire design defect', 'tire belt separation',
            'tire sidewall failure', 'tire explosion', 'truck tire blowout',
            'motorcycle tire failure', 'used tire defect',
            
            # Legal context
            'tire defect lawyer', 'tire blowout attorney', 'tire manufacturer liability',
            'tire defect lawsuit', 'tire recall claim', 'tire failure settlement'
        ],
        
        'appliance_defects': [
            # Core terms
            'defective appliance', 'appliance malfunction', 'home appliance injury',
            'appliance defect', 'appliance recall', 'faulty appliance',
            
            # Specific appliances
            'defective refrigerator', 'washing machine defect', 'dryer fire', 'dishwasher leak',
            'oven explosion', 'microwave fire', 'toaster fire', 'coffee maker defect',
            'water heater explosion', 'air conditioner defect', 'vacuum cleaner defect',
            
            # Legal context
            'appliance defect lawyer', 'home appliance attorney', 'appliance manufacturer liability',
            'appliance recall lawsuit', 'appliance defect claim'
        ],
    },

    # 5. Medical & Healthcare Malpractice
    'medical_healthcare_malpractice': {
        'medical_malpractice': [
            # Core terms
            'medical malpractice', 'medical negligence', 'doctor negligence', 'physician negligence',
            'hospital negligence', 'healthcare malpractice', 'healthcare negligence',
            'medical error', 'doctor error', 'physician malpractice', 'medical mistake',
            
            # Standard of care
            'breach of standard of care', 'substandard medical care', 'negligent medical treatment',
            'medical professional negligence', 'healthcare provider negligence',
            
            # Legal context
            'medical malpractice lawyer', 'medical negligence attorney', 'malpractice lawsuit',
            'medical malpractice claim', 'doctor malpractice suit', 'hospital malpractice suit',
            'medical expert witness', 'standard of care violation'
        ],
        
        'misdiagnosis': [
            # Core terms
            'misdiagnosis', 'missed diagnosis', 'delayed diagnosis', 'wrong diagnosis',
            'failure to diagnose', 'diagnostic error', 'diagnostic negligence',
            'misdiagnosed condition', 'diagnostic malpractice',
            
            # Specific conditions
            'cancer misdiagnosis', 'heart attack misdiagnosis', 'stroke misdiagnosis',
            'infection misdiagnosis', 'diabetes misdiagnosis', 'appendicitis misdiagnosis',
            'blood clot misdiagnosis', 'pneumonia misdiagnosis',
            
            # Legal context
            'misdiagnosis lawyer', 'diagnostic error attorney', 'failure to diagnose lawsuit',
            'delayed diagnosis claim', 'misdiagnosis malpractice suit'
        ],
        
        'surgery_mistakes': [
            # Core terms
            'surgical error', 'surgical negligence', 'botched surgery', 'surgery mistake',
            'surgical malpractice', 'operating room error', 'surgeon negligence',
            
            # Specific errors
            'wrong site surgery', 'wrong patient surgery', 'wrong procedure',
            'retained surgical instrument', 'surgical sponge left behind',
            'nerve damage surgery', 'organ damage surgery', 'surgical infection',
            'anesthesia error surgery', 'post-operative negligence',
            
            # Surgery types
            'cardiac surgery error', 'brain surgery error', 'orthopedic surgery error',
            'plastic surgery malpractice', 'cosmetic surgery negligence',
            'emergency surgery error', 'outpatient surgery error',
            
            # Legal context
            'surgical malpractice lawyer', 'surgery error attorney', 'botched surgery lawsuit',
            'surgical negligence claim', 'operating room malpractice'
        ],
        
        'medication_errors': [
            # Core terms
            'medication error', 'prescription error', 'pharmacy error',
            'wrong medication', 'wrong prescription', 'incorrect medication',
            'wrong dosage', 'incorrect dosage', 'overdose', 'underdose',
            
            # Specific errors
            'pharmacy dispensing error', 'hospital medication error', 'nursing medication error',
            'IV medication error', 'drug interaction error', 'allergy medication error',
            'pediatric dosing error', 'chemotherapy dosing error',
            
            # Legal context
            'medication error lawyer', 'pharmacy malpractice attorney', 'prescription error lawsuit',
            'pharmacist negligence', 'hospital medication negligence', 'nurse medication error'
        ],
        
        'birth_injuries': [
            # Core terms
            'birth injury', 'birth trauma', 'childbirth injury', 'delivery injury',
            'obstetric injury', 'labor and delivery injury', 'newborn injury',
            'maternal injury', 'birthing injury', 'perinatal injury',
            
            # Specific injuries
            'cerebral palsy', 'erb palsy', 'brachial plexus injury', 'shoulder dystocia',
            'brain damage birth', 'oxygen deprivation birth', 'hypoxic ischemic encephalopathy',
            'facial nerve palsy birth', 'fracture during birth', 'vacuum extraction injury',
            'forceps delivery injury', 'c-section injury',
            
            # Legal context
            'birth injury lawyer', 'birth trauma attorney', 'obstetric malpractice lawyer',
            'delivery malpractice', 'childbirth negligence', 'labor and delivery malpractice',
            'birth injury lawsuit', 'cerebral palsy lawyer'
        ],
        
        'nursing_home_neglect': [
            # Core terms
            'nursing home abuse', 'nursing home neglect', 'elder care negligence',
            'long term care abuse', 'assisted living abuse', 'skilled nursing facility abuse',
            'nursing home malpractice', 'elder abuse nursing home',
            
            # Types of abuse/neglect
            'nursing home physical abuse', 'nursing home sexual abuse', 'nursing home emotional abuse',
            'nursing home financial abuse', 'medication neglect nursing home',
            'hygiene neglect nursing home', 'nutrition neglect nursing home',
            
            # Specific issues
            'nursing home bedsores', 'pressure ulcers nursing home', 'nursing home falls',
            'nursing home dehydration', 'nursing home malnutrition', 'nursing home infection',
            'nursing home wandering', 'nursing home elopement',
            
            # Legal context
            'nursing home abuse lawyer', 'elder abuse attorney', 'nursing home negligence lawyer',
            'long term care lawsuit', 'nursing home wrongful death'
        ],
        
        'dental_mistakes': [
            # Core terms
            'dental malpractice', 'dental negligence', 'dentist negligence', 'dental error',
            'botched dental work', 'dental mistake', 'oral surgery error',
            
            # Specific errors
            'wrong tooth extraction', 'nerve damage dental', 'dental drill injury',
            'dental infection', 'failed root canal', 'dental implant failure',
            'orthodontic negligence', 'dental anesthesia error', 'dental X-ray error',
            
            # Legal context
            'dental malpractice lawyer', 'dentist negligence attorney', 'dental error lawsuit',
            'oral surgery malpractice', 'orthodontic malpractice'
        ],
        
        'vaccine_injuries': [
            # Core terms
            'vaccine injury', 'vaccination injury', 'vaccine adverse event', 'vaccine reaction',
            'vaccine side effect', 'immunization injury', 'vaccine complication',
            
            # Specific reactions
            'vaccine allergic reaction', 'vaccine anaphylaxis', 'vaccine seizure',
            'vaccine encephalitis', 'vaccine shoulder injury', 'SIRVA vaccine',
            'vaccine autism claim', 'vaccine brain injury',
            
            # Legal context
            'vaccine injury lawyer', 'vaccination injury attorney', 'vaccine court',
            'VICP claim', 'vaccine compensation program', 'vaccine injury petition'
        ],
        
        'hospital_infections': [
            # Core terms
            'hospital acquired infection', 'nosocomial infection', 'healthcare associated infection',
            'hospital infection', 'post-operative infection', 'surgical site infection',
            
            # Specific infections
            'MRSA infection', 'staph infection hospital', 'C. diff infection', 'sepsis hospital',
            'pneumonia hospital', 'urinary tract infection hospital', 'bloodstream infection hospital',
            'catheter infection', 'ventilator pneumonia',
            
            # Legal context
            'hospital infection lawyer', 'nosocomial infection attorney', 'hospital acquired infection lawsuit',
            'infection control negligence', 'hospital hygiene negligence'
        ],
        
        'emergency_room_errors': [
            # Core terms
            'emergency room malpractice', 'ER malpractice', 'emergency room negligence',
            'ER negligence', 'emergency department error', 'urgent care negligence',
            
            # Specific errors
            'delayed treatment ER', 'failure to treat emergency', 'ER misdiagnosis',
            'emergency room discharge error', 'triage negligence', 'emergency room understaffing',
            'EMTALA violation', 'patient dumping', 'emergency transfer negligence',
            
            # Legal context
            'emergency room lawyer', 'ER malpractice attorney', 'emergency medicine negligence',
            'emergency department lawsuit', 'urgent care malpractice'
        ],
        
        'anesthesia_errors': [
            # Core terms
            'anesthesia malpractice', 'anesthesia error', 'anesthesia negligence',
            'anesthesiologist negligence', 'anesthesia complications', 'anesthesia mistake',
            
            # Specific errors
            'anesthesia overdose', 'anesthesia underdose', 'failed intubation',
            'anesthesia awareness', 'oxygen deprivation anesthesia', 'anesthesia allergic reaction',
            'anesthesia drug error', 'monitoring failure anesthesia',
            
            # Legal context
            'anesthesia malpractice lawyer', 'anesthesia error attorney', 'anesthesiologist malpractice',
            'anesthesia negligence lawsuit', 'anesthesia complication claim'
        ],
        
        'psychiatric_malpractice': [
            # Core terms
            'psychiatric malpractice', 'mental health negligence', 'psychiatrist negligence',
            'psychologist malpractice', 'therapy malpractice', 'counselor negligence',
            
            # Specific issues
            'wrongful commitment', 'psychiatric medication error', 'suicide psychiatric negligence',
            'sexual abuse therapist', 'breach of confidentiality', 'abandonment of patient',
            'misdiagnosis psychiatric', 'psychiatric hospitalization negligence',
            
            # Legal context
            'psychiatric malpractice lawyer', 'mental health negligence attorney',
            'therapist malpractice lawsuit', 'psychiatric negligence claim'
        ],
        
        'telehealth_negligence': [
            # Core terms
            'telehealth negligence', 'telemedicine malpractice', 'virtual doctor mistake',
            'online diagnosis error', 'remote care malpractice', 'telehealth error',
            
            # Specific issues
            'telehealth misdiagnosis', 'virtual consultation negligence', 'remote monitoring failure',
            'telehealth prescription error', 'video consultation error', 'telehealth technology failure',
            
            # Legal context
            'telehealth malpractice lawyer', 'telemedicine negligence attorney',
            'virtual care lawsuit', 'remote medicine malpractice'
        ],
        
        'elder_abuse': [
            # Core terms
            'elder abuse', 'senior abuse', 'elderly abuse', 'elder neglect',
            'elderly neglect', 'senior neglect', 'elder mistreatment', 'geriatric abuse',
            
            # Types of abuse
            'elder physical abuse', 'elder sexual abuse', 'elder emotional abuse',
            'financial elder abuse', 'elder financial exploitation', 'elder abandonment',
            'elder self-neglect', 'caregiver abuse elder',
            
            # Settings
            'home care elder abuse', 'adult day care abuse', 'assisted living abuse',
            'hospital elder abuse', 'rehabilitation facility elder abuse',
            
            # Legal context
            'elder abuse lawyer', 'senior abuse attorney', 'elder neglect lawsuit',
            'financial exploitation attorney', 'elder rights violation'
        ],
    },

    # 6. Workplace Injuries
    'workplace_injuries': {
        'workers_compensation': [
            # Core terms
            'workers compensation', 'workers comp', 'work comp', 'workplace compensation',
            'workplace injury', 'work injury', 'injured on the job', 'occupational injury',
            'job injury', 'employment injury', 'work related injury', 'on the job injury',
            
            # Specific claims
            'workers comp claim', 'work comp benefits', 'disability benefits work',
            'temporary disability work', 'permanent disability work', 'medical benefits work comp',
            'vocational rehabilitation work comp', 'return to work injury',
            
            # Railroad workers (FELA) - MOVED from train accidents as requested
            'railroad worker injury', 'train crew injury', 'locomotive engineer injury',
            'railroad employee accident', 'train conductor injury', 'railroad maintenance worker injury',
            'train yard worker accident', 'railroad workplace injury', 'FELA claim',
            'FELA lawsuit', 'railroad negligence FELA', 'federal employers liability act',
            
            # Legal context
            'workers compensation lawyer', 'work comp attorney', 'workplace injury lawyer',
            'workers comp denial', 'work comp dispute', 'workers compensation appeal',
            'third party work injury', 'work injury lawsuit'
        ],
        
        'construction_site_injury': [
            # Core terms - REMOVED generic workplace terms to avoid overlap
            'construction accident', 'construction site injury', 'construction site accident', 
            'building site injury', 'construction zone accident', 'job site injury',
            
            # Specific accidents
            'construction fall', 'scaffolding accident', 'ladder accident construction',
            'crane accident', 'heavy equipment accident', 'excavation accident',
            'trenching accident', 'roof work accident', 'construction electrocution',
            'construction burn injury', 'falling object construction',
            
            # Equipment-related
            'power tool accident construction', 'construction machinery accident',
            'bulldozer accident', 'forklift accident construction', 'concrete mixer accident',
            'nail gun accident', 'saw accident construction',
            
            # Legal context
            'construction accident lawyer', 'construction injury attorney', 'construction site negligence',
            'contractor negligence', 'construction safety violation', 'OSHA violation construction',
            'construction third party claim', 'construction site lawsuit'
        ],
        
        'industrial_accidents': [
            # Core terms
            'industrial accident', 'industrial injury', 'factory accident', 'plant accident',
            'manufacturing accident', 'warehouse accident', 'mill accident',
            
            # Specific accidents
            'assembly line injury', 'assembly line accident', 'machinery accident industrial',
            'conveyor belt accident', 'industrial burn', 'chemical burn industrial',
            'industrial explosion', 'industrial fire', 'industrial fall',
            
            # Equipment-related
            'industrial machinery accident', 'press machine accident', 'grinder accident',
            'industrial robot accident', 'forklift accident industrial', 'crane accident industrial',
            
            # Legal context
            'industrial accident lawyer', 'factory accident attorney', 'industrial negligence',
            'manufacturing injury lawyer', 'industrial safety violation', 'workplace safety negligence'
        ],
        
        'toxic_exposure': [
            # Core terms
            'toxic exposure work', 'occupational exposure', 'workplace chemical exposure',
            'toxic substance exposure', 'hazardous material exposure', 'chemical exposure work',
            
            # Specific substances
            'asbestos exposure work', 'lead exposure work', 'silica exposure', 'benzene exposure',
            'formaldehyde exposure', 'pesticide exposure work', 'solvent exposure',
            'radioactive substance exposure', 'heavy metal exposure', 'industrial chemical exposure',
            
            # Health effects
            'occupational lung disease', 'chemical poisoning work', 'industrial disease',
            'workplace cancer', 'occupational asthma', 'dermatitis work',
            
            # Legal context
            'toxic exposure lawyer', 'occupational disease attorney', 'workplace exposure lawsuit',
            'industrial disease claim', 'occupational illness lawyer'
        ],
        
        'office_injuries': [
            # Core terms
            'office injury', 'office accident', 'workplace slip and fall', 'office slip and fall',
            'cubicle injury', 'desk injury', 'office chair accident',
            
            # Specific injuries
            'repetitive strain injury', 'RSI work', 'carpal tunnel work', 'carpal tunnel from work',
            'computer injury', 'keyboard injury', 'mouse injury RSI', 'typing injury',
            'office ergonomic injury', 'back injury office chair', 'neck injury computer',
            
            # Office hazards
            'office equipment injury', 'filing cabinet accident', 'office furniture accident',
            'office electrical accident', 'office fire injury', 'office air quality injury',
            
            # Legal context
            'office injury lawyer', 'repetitive strain attorney', 'ergonomic injury lawyer',
            'office workers comp', 'carpal tunnel workers comp', 'office negligence lawsuit'
        ],
    },

    # 7. Catastrophic & Severe Injuries
    'catastrophic_severe_injuries': {
        'brain_injury': [
            # Core terms
            'brain injury', 'traumatic brain injury', 'TBI', 'head injury', 'head trauma',
            'brain trauma', 'closed head injury', 'open head injury', 'skull fracture',
            
            # Specific types
            'concussion', 'post-concussion syndrome', 'severe brain injury', 'mild brain injury',
            'moderate brain injury', 'diffuse axonal injury', 'brain contusion', 'brain hemorrhage',
            'subdural hematoma', 'epidural hematoma', 'coup contrecoup injury',
            
            # Causes
            'car accident brain injury', 'fall brain injury', 'sports concussion',
            'workplace head injury', 'assault brain injury', 'medical malpractice brain injury',
            
            # Effects
            'cognitive impairment', 'memory loss brain injury', 'personality change brain injury',
            'brain injury disability', 'vegetative state', 'coma brain injury',
            
            # Legal context
            'brain injury lawyer', 'TBI attorney', 'traumatic brain injury lawyer',
            'head injury lawsuit', 'brain injury compensation', 'TBI settlement'
        ],
        
        'spinal_injury': [
            # Core terms
            'spinal injury', 'spinal cord injury', 'spine injury', 'back injury',
            'neck injury', 'cervical spine injury', 'lumbar spine injury', 'thoracic spine injury',
            
            # Specific injuries
            'paralysis', 'paraplegia', 'quadriplegia', 'tetraplegia', 'incomplete spinal injury',
            'complete spinal injury', 'spinal fracture', 'herniated disc', 'bulging disc',
            'disc herniation', 'spinal stenosis', 'nerve damage spine',
            
            # Causes
            'car accident spinal injury', 'fall spinal injury', 'diving accident paralysis',
            'sports spinal injury', 'workplace back injury', 'lifting injury back',
            
            # Legal context
            'spinal injury lawyer', 'paralysis attorney', 'spinal cord injury lawyer',
            'back injury lawsuit', 'spinal injury compensation', 'paralysis settlement'
        ],
        
        'burn_injuries': [
            # Core terms - REMOVED standalone "fire injury"
            'burn injury', 'severe burns', 'thermal injury',
            'scald injury', 'electrical burn', 'chemical burn', 'radiation burn',
            'burn accident', 'fire burn injury', 'flame burn injury',
            
            # Burn degrees
            'first degree burn', 'second degree burn', 'third degree burn', 'fourth degree burn',
            'full thickness burn', 'partial thickness burn', 'superficial burn',
            
            # Causes
            'house fire burn', 'car fire burn', 'workplace burn', 'electrical accident burn',
            'scalding water burn', 'hot oil burn', 'steam burn', 'explosion burn',
            'chemical spill burn', 'acid burn', 'grease fire burn',
            
            # Treatment
            'burn center treatment', 'skin graft burn', 'burn reconstruction surgery',
            'burn scar', 'burn disfigurement', 'burn rehabilitation',
            
            # Legal context
            'burn injury lawyer', 'fire accident attorney', 'burn injury lawsuit',
            'burn injury compensation', 'fire injury settlement', 'burn negligence case'
        ],
        
        'amputation': [
            # Core terms
            'amputation', 'loss of limb', 'limb loss', 'dismemberment', 'severed limb',
            'traumatic amputation', 'surgical amputation', 'partial amputation',
            
            # Specific amputations
            'loss of arm', 'arm amputation', 'loss of leg', 'leg amputation',
            'loss of hand', 'hand amputation', 'loss of foot', 'foot amputation',
            'finger amputation', 'toe amputation', 'digit amputation',
            
            # Causes
            'machinery amputation', 'car accident amputation', 'workplace amputation',
            'construction accident amputation', 'medical malpractice amputation',
            'infection amputation', 'crush injury amputation',
            
            # Legal context
            'amputation lawyer', 'limb loss attorney', 'amputation lawsuit',
            'amputation compensation', 'limb loss settlement', 'dismemberment claim'
        ],
        
        'internal_organ_injury': [
            # Core terms
            'internal organ injury', 'internal injury', 'organ damage', 'internal trauma',
            'abdominal injury', 'chest injury', 'internal bleeding', 'organ laceration',
            
            # Specific organs
            'liver injury', 'kidney injury', 'spleen injury', 'lung injury',
            'heart injury', 'stomach injury', 'intestinal injury', 'pancreas injury',
            'bladder injury', 'diaphragm injury',
            
            # Causes
            'car accident internal injury', 'fall internal injury', 'assault internal injury',
            'medical malpractice organ damage', 'workplace internal injury',
            'sports internal injury', 'blunt force trauma',
            
            # Legal context
            'internal injury lawyer', 'organ damage attorney', 'internal trauma lawsuit',
            'internal injury compensation', 'organ injury settlement'
        ],
        
        'wrongful_death': [
            # Core terms - REMOVED standalone "accident"
            'wrongful death', 'fatal accident', 'death claim', 'accidental death',
            'wrongful death lawsuit', 'survivor benefits', 'death benefits',
            'funeral expenses', 'burial costs', 'loss of consortium',
            
            # Causes
            'car accident death', 'medical malpractice death', 'workplace death',
            'product liability death', 'premises liability death', 'construction accident death',
            'nursing home death', 'hospital negligence death', 'drug recall death',
            
            # Survivors
            'spouse wrongful death', 'child wrongful death', 'parent wrongful death',
            'family wrongful death', 'dependent wrongful death', 'estate wrongful death',
            
            # Legal context
            'wrongful death lawyer', 'wrongful death attorney', 'fatal accident lawyer',
            'wrongful death settlement', 'wrongful death compensation', 'survival action',
            'estate claim', 'loss of income death', 'loss of support death'
        ],
    },

    # 8. Mass Tort & Class Action Lawsuits
    'mass_tort_class_action_lawsuits': {
        'mass_tort': [
            # Core terms
            'mass tort', 'class action', 'class action lawsuit', 'multi-district litigation',
            'MDL', 'mass litigation', 'aggregate litigation', 'consolidated lawsuit',
            'bellwether trial', 'mass tort settlement', 'class action settlement',
            
            # Legal context
            'mass tort lawyer', 'class action attorney', 'MDL attorney',
            'mass tort litigation', 'class action claim', 'opt out class action',
            'class certification', 'mass tort compensation'
        ],
        
        'mesothelioma': [
            # Core terms
            'mesothelioma', 'asbestos cancer', 'asbestos disease', 'pleural mesothelioma',
            'peritoneal mesothelioma', 'pericardial mesothelioma', 'testicular mesothelioma',
            
            # Asbestos exposure
            'asbestos', 'asbestos exposure', 'occupational asbestos exposure',
            'asbestos exposure work', 'asbestos exposure home', 'secondary asbestos exposure',
            'asbestos products', 'asbestos insulation', 'asbestos ceiling tiles',
            'asbestos brake pads', 'asbestos shipyard', 'asbestos construction',
            
            # Legal context
            'mesothelioma lawyer', 'asbestos attorney', 'mesothelioma lawsuit',
            'asbestos trust fund', 'mesothelioma settlement', 'asbestos compensation',
            'mesothelioma claim', 'asbestos litigation'
        ],
        
        'lead_poisoning': [
            # Core terms
            'lead poisoning', 'lead exposure', 'childhood lead poisoning', 'lead contamination',
            'elevated blood lead', 'lead toxicity', 'lead intoxication',
            
            # Sources
            'lead paint exposure', 'lead based paint', 'lead paint chips', 'lead dust exposure',
            'lead water pipes', 'lead plumbing', 'lead in water', 'lead soil contamination',
            'lead toys', 'lead jewelry', 'lead ceramics',
            
            # Effects
            'lead poisoning children', 'developmental delays lead', 'learning disabilities lead',
            'behavioral problems lead', 'cognitive impairment lead', 'lead poisoning pregnancy',
            
            # Legal context
            'lead poisoning lawyer', 'lead paint attorney', 'lead exposure lawsuit',
            'lead paint lawsuit', 'lead poisoning settlement', 'lead exposure compensation'
        ],
        
        'hernia_mesh': [
            # Core terms
            'hernia mesh', 'surgical mesh', 'hernia mesh complication', 'defective hernia mesh',
            'hernia mesh failure', 'hernia mesh recall', 'mesh implant',
            
            # Complications
            'mesh erosion', 'mesh migration', 'mesh infection', 'mesh adhesion',
            'mesh shrinkage', 'chronic pain mesh', 'bowel obstruction mesh',
            'mesh revision surgery', 'mesh removal surgery',
            
            # Legal context
            'hernia mesh lawyer', 'surgical mesh attorney', 'hernia mesh lawsuit',
            'mesh complication claim', 'hernia mesh settlement', 'defective mesh litigation'
        ],
        
        'proton_pump': [
            # Core terms
            'proton pump inhibitors', 'proton-pump inhibitors', 'PPI', 'PPI lawsuit',
            'acid reflux medication', 'heartburn medication', 'GERD medication',
            
            # Specific medications
            'nexium', 'prilosec', 'prevacid', 'protonix', 'aciphex', 'dexilant',
            'omeprazole', 'esomeprazole', 'lansoprazole', 'pantoprazole',
            
            # Side effects
            'PPI kidney damage', 'PPI bone fractures', 'PPI dementia', 'PPI heart attack',
            'chronic kidney disease PPI', 'osteoporosis PPI', 'magnesium deficiency PPI',
            
            # Legal context
            'PPI lawyer', 'proton pump inhibitor attorney', 'nexium lawsuit',
            'prilosec lawsuit', 'PPI kidney lawsuit', 'acid reflux drug lawsuit'
        ],
        
        'firefighting_foam': [
            # Core terms
            'firefighting foam', 'firefighter foam', 'AFFF', 'aqueous film forming foam',
            'PFAS foam', 'PFOA foam', 'PFOS foam', 'firefighting chemicals',
            
            # Exposure
            'firefighter PFAS exposure', 'military base contamination', 'airport firefighting foam',
            'foam contamination water', 'PFAS water contamination', 'foam training exposure',
            
            # Health effects
            'PFAS cancer', 'firefighting foam cancer', 'kidney cancer PFAS', 'liver cancer PFAS',
            'thyroid disease PFAS', 'ulcerative colitis PFAS',
            
            # Legal context
            'firefighting foam lawyer', 'AFFF attorney', 'PFAS lawsuit',
            'firefighting foam cancer lawsuit', 'AFFF contamination claim'
        ],
        
        'hair_relaxer': [
            # Core terms
            'hair relaxer', 'hair relaxant', 'chemical hair straightener', 'relaxer lawsuit',
            'hair straightening products', 'chemical relaxer',
            
            # Health effects
            'hair relaxer cancer', 'uterine cancer hair relaxer', 'ovarian cancer hair relaxer',
            'endometrial cancer hair relaxer', 'breast cancer hair relaxer',
            'fibroids hair relaxer', 'early puberty hair relaxer',
            
            # Legal context
            'hair relaxer lawyer', 'hair straightener attorney', 'relaxer cancer lawsuit',
            'chemical hair relaxer lawsuit', 'hair relaxer settlement'
        ],
        
        'ozempic': [
            # Core terms
            'ozempic', 'semaglutide', 'wegovy', 'rybelsus', 'GLP-1', 'GLP-1 agonist',
            'diabetes medication', 'weight loss drug',
            
            # Side effects
            'ozempic gastroparesis', 'ozempic stomach paralysis', 'ozempic bowel obstruction',
            'ozempic pancreatitis', 'ozempic gallbladder', 'ozempic thyroid cancer',
            'ozempic kidney problems', 'ozempic nausea', 'ozempic vomiting',
            
            # Legal context
            'ozempic lawyer', 'semaglutide attorney', 'GLP-1 lawsuit',
            'ozempic gastroparesis lawsuit', 'wegovy lawsuit', 'diabetes drug lawsuit'
        ],
        
        'roundup': [
            # Core terms
            'roundup', 'glyphosate', 'roundup weed killer', 'roundup herbicide',
            'glyphosate exposure', 'roundup exposure', 'weed killer cancer',
            
            # Cancer types
            'roundup non-hodgkin lymphoma', 'roundup NHL', 'glyphosate cancer',
            'roundup leukemia', 'roundup lymphoma', 'monsanto roundup cancer',
            
            # Exposure
            'agricultural roundup exposure', 'landscaping roundup exposure',
            'home gardening roundup', 'occupational glyphosate exposure',
            
            # Legal context
            'roundup lawyer', 'glyphosate attorney', 'roundup cancer lawsuit',
            'monsanto lawsuit', 'roundup settlement', 'weed killer lawsuit'
        ],
        
        'camp_lejeune': [
            # Core terms
            'camp lejeune', 'camp lejeune water contamination', 'marine base contamination',
            'camp lejeune toxic water', 'lejeune contamination', 'camp lejeune chemicals',
            
            # Chemicals
            'TCE contamination', 'PCE contamination', 'benzene contamination camp lejeune',
            'vinyl chloride contamination', 'contaminated drinking water camp lejeune',
            
            # Health effects
            'camp lejeune cancer', 'camp lejeune leukemia', 'camp lejeune birth defects',
            'camp lejeune kidney cancer', 'camp lejeune liver cancer',
            'camp lejeune bladder cancer', 'camp lejeune parkinson disease',
            
            # Legal context
            'camp lejeune lawyer', 'camp lejeune attorney', 'camp lejeune lawsuit',
            'camp lejeune justice act', 'camp lejeune claim', 'marine contamination lawsuit'
        ],
        
        'suboxone': [
            # Core terms
            'suboxone', 'buprenorphine', 'suboxone film', 'suboxone strips',
            'opioid addiction treatment', 'suboxone medication',
            
            # Dental problems
            'suboxone tooth decay', 'suboxone dental problems', 'suboxone teeth falling out',
            'suboxone tooth loss', 'suboxone dental damage', 'suboxone tooth extraction',
            'suboxone oral health', 'suboxone cavities',
            
            # Legal context
            'suboxone lawyer', 'suboxone attorney', 'suboxone tooth decay lawsuit',
            'suboxone dental lawsuit', 'buprenorphine lawsuit', 'suboxone settlement'
        ],
        
        'biozorb_implant': [
            # Core terms
            'biozorb implant', 'biozorb marker', 'breast surgery marker', 'surgical marker implant',
            'biozorb device', 'focal therapeutics biozorb',
            
            # Complications
            'biozorb migration', 'biozorb infection', 'biozorb pain', 'biozorb inflammation',
            'biozorb removal surgery', 'biozorb complication', 'biozorb revision',
            
            # Legal context
            'biozorb lawyer', 'biozorb attorney', 'biozorb lawsuit',
            'biozorb implant lawsuit', 'surgical marker lawsuit', 'biozorb settlement'
        ],
    },

    # 9. Intentional Torts & Personal Rights Violations
    'intentional_torts_personal_rights_violations': {
        'false_imprisonment': [
            # Core terms
            'false imprisonment', 'unlawful detention', 'wrongful confinement',
            'illegal detention', 'unlawful restraint', 'false arrest', 'wrongful arrest',
            'kidnapping', 'unlawful confinement', 'wrongful imprisonment',
            
            # Legal context
            'false imprisonment lawsuit', 'unlawful detention claim', 'false arrest lawsuit',
            'wrongful confinement attorney', 'false imprisonment lawyer'
        ],
        
        'invasion_of_privacy': [
            # Core terms
            'invasion of privacy', 'privacy violation', 'breach of privacy',
            'unauthorized recording', 'illegal surveillance', 'wiretapping',
            'hidden camera', 'invasion of solitude', 'public disclosure private facts',
            
            # Digital privacy
            'data breach', 'identity theft', 'unauthorized data collection',
            'privacy invasion online', 'social media privacy violation',
            
            # Legal context
            'privacy violation lawsuit', 'invasion of privacy attorney',
            'privacy rights violation', 'privacy lawsuit', 'surveillance lawsuit'
        ],
        
        'assault_battery': [
            # Core terms - REMOVED standalone "battery" 
            'assault', 'assault and battery', 'assault victim', 'battery victim',
            'victim of violence', 'physically assaulted', 'physical attack', 'violent assault',
            
            # Types
            'aggravated assault', 'simple assault', 'domestic violence', 'bar fight',
            'street assault', 'workplace violence', 'random attack', 'unprovoked assault',
            
            # Legal context
            'assault lawsuit', 'battery lawsuit', 'assault and battery attorney',
            'assault victim lawyer', 'violence lawsuit', 'assault compensation'
        ],
        
        'sexual_assault': [
            # Core terms
            'sexual assault', 'sexual abuse', 'sexual battery', 'rape',
            'sexual harassment', 'sexual misconduct', 'sexual violence',
            'unwanted sexual contact', 'sexual exploitation',
            
            # Institutional
            'workplace sexual harassment', 'school sexual assault', 'college sexual assault',
            'church sexual abuse', 'scout sexual abuse', 'sports sexual abuse',
            'prison sexual assault', 'military sexual assault',
            
            # Legal context
            'sexual assault lawyer', 'sexual abuse attorney', 'sexual harassment lawsuit',
            'sexual assault claim', 'sexual abuse compensation', 'title ix lawsuit'
        ],
        
        'emotional_distress': [
            # Core terms
            'emotional distress', 'psychological trauma', 'mental anguish', 'emotional trauma',
            'psychological distress', 'mental suffering', 'emotional harm',
            'intentional infliction emotional distress', 'negligent infliction emotional distress',
            
            # PTSD and related
            'PTSD from incident', 'post traumatic stress', 'anxiety from incident',
            'depression from trauma', 'psychological injury', 'mental health damage',
            
            # Legal context
            'emotional distress lawsuit', 'psychological trauma attorney',
            'mental anguish claim', 'emotional distress compensation',
            'psychological injury lawyer'
        ],
        
        'police_misconduct': [
            # Core terms
            'police brutality', 'police misconduct', 'excessive force', 'police violence',
            'civil rights violation', 'police abuse', 'unlawful arrest', 'police negligence',
            
            # Specific violations
            'wrongful death police', 'police shooting', 'police taser', 'police chokehold',
            'racial profiling', 'search and seizure violation', 'miranda rights violation',
            'police corruption', 'false arrest police',
            
            # Legal context
            'police brutality lawyer', 'excessive force attorney', 'civil rights lawyer',
            'police misconduct lawsuit', '1983 lawsuit', 'section 1983 claim',
            'civil rights violation attorney'
        ],
        
        'government_negligence': [
            # Core terms
            'government negligence', 'municipal negligence', 'city negligence',
            'county negligence', 'state negligence', 'government liability',
            'public entity negligence', 'sovereign immunity waiver',
            
            # Specific areas
            'road maintenance negligence', 'public property negligence', 'government facility negligence',
            'public works negligence', 'government employee negligence',
            'municipal services negligence', 'public safety negligence',
            
            # Legal context
            'government negligence lawyer', 'municipal liability attorney',
            'government lawsuit', 'public entity claim', 'sovereign immunity lawsuit'
        ],
        
        'cyber_harassment': [
            # Core terms
            'cyberbullying', 'online harassment', 'cyber stalking', 'internet harassment',
            'digital harassment', 'online abuse', 'cyber abuse', 'electronic harassment',
            
            # Specific types
            'revenge porn', 'deepfake harassment', 'doxxing', 'online threats',
            'social media harassment', 'email harassment', 'text harassment',
            'cyberstalking', 'online impersonation', 'digital stalking',
            
            # Legal context
            'cyberbullying lawyer', 'online harassment attorney', 'cyber stalking lawsuit',
            'revenge porn lawyer', 'digital harassment claim', 'cyberbullying lawsuit'
        ],
    },

    # 10. Sports & Recreational Injuries
    'sports_recreational_injuries': {
        'recreational_facility_injuries': [
            # Facility injuries - REMOVED generic "sports injury" to avoid overlap with child category
            'gym accident', 'fitness center injury', 'health club injury', 'YMCA injury',
            'recreation center injury', 'sports complex injury', 'athletic facility injury',
            'recreational facility accident', 'fitness facility negligence',
            
            # Equipment-related
            'defective sports equipment', 'sports equipment failure', 'faulty sports gear',
            'protective equipment failure', 'sports equipment recall', 'helmet failure sports',
            'exercise equipment accident', 'weight machine accident', 'treadmill accident',
            
            # Supervision
            'coach negligence', 'inadequate sports supervision', 'referee negligence',
            'sports instructor negligence', 'trainer negligence', 'athletic trainer negligence',
            
            # Legal context
            'recreational facility lawyer', 'gym accident attorney', 'fitness center negligence',
            'sports facility negligence', 'recreational injury claim', 'athletic facility lawsuit'
        ],
        
        'water_sports_injuries': [
            # Core terms
            'water sports injury', 'aquatic injury', 'water recreation injury',
            'marine sports injury', 'water activity injury',
            
            # Specific activities
            'jet ski accident', 'jetski injury', 'personal watercraft accident',
            'water skiing accident', 'wakeboarding injury', 'surfing injury',
            'diving accident', 'scuba diving injury', 'snorkeling accident',
            'kayaking accident', 'canoeing injury', 'rafting accident',
            
            # Legal context
            'water sports lawyer', 'jet ski accident attorney', 'diving accident lawyer',
            'water recreation lawsuit', 'aquatic injury claim', 'marine sports negligence'
        ],
        
        'extreme_sports_injuries': [
            # Core terms
            'extreme sports injury', 'adventure sports injury', 'extreme recreation injury',
            'adrenaline sports injury', 'action sports injury',
            
            # Specific sports
            'skydiving accident', 'bungee jumping accident', 'rock climbing injury',
            'mountain climbing accident', 'base jumping accident', 'paragliding accident',
            'hang gliding injury', 'zip line accident', 'bungee cord failure',
            
            # Ground sports
            'skateboarding accident', 'skateboard injury', 'longboard accident',
            'snowboarding injury', 'skiing accident', 'mountain biking injury',
            'BMX accident', 'motocross injury', 'dirt bike accident',
            
            # Legal context
            'extreme sports lawyer', 'adventure sports attorney', 'skydiving accident lawyer',
            'extreme sports negligence', 'assumption of risk sports', 'waiver enforcement sports'
        ],
    },

    # 11. Environmental & Toxic Exposure Injuries
    'environmental_toxic_exposure_injuries': {
        'environmental_exposure': [
            # Core terms
            'environmental exposure', 'toxic exposure', 'chemical exposure', 'environmental contamination',
            'pollution exposure', 'hazardous waste exposure', 'industrial contamination',
            'environmental poisoning', 'toxic contamination', 'chemical contamination',
            
            # Sources
            'groundwater contamination', 'air pollution exposure', 'soil contamination',
            'industrial pollution', 'chemical plant exposure', 'factory contamination',
            'landfill contamination', 'superfund site exposure',
            
            # Legal context
            'environmental exposure lawyer', 'toxic exposure attorney', 'contamination lawsuit',
            'environmental contamination claim', 'pollution exposure lawsuit'
        ],
        
        'toxic_mold_exposure': [
            # Core terms
            'toxic mold exposure', 'mold exposure', 'mold illness', 'mold poisoning',
            'black mold exposure', 'black mold injury', 'stachybotrys exposure',
            'mold contamination', 'indoor mold exposure', 'mold toxicity',
            
            # Health effects
            'mold allergic reaction', 'mold respiratory problems', 'mold asthma',
            'mold neurological symptoms', 'mold cognitive problems', 'mold headaches',
            'sick building syndrome', 'mold sensitivity',
            
            # Legal context
            'mold exposure lawyer', 'toxic mold attorney', 'black mold lawsuit',
            'mold contamination claim', 'landlord mold negligence', 'mold remediation negligence'
        ],
        
        'carbon_monoxide_poisoning': [
            # Core terms
            'carbon monoxide poisoning', 'carbon monoxide exposure', 'CO poisoning',
            'carbon monoxide leak', 'carbon monoxide leak injury', 'CO exposure',
            'carbon monoxide intoxication', 'CO leak accident',
            
            # Sources
            'furnace carbon monoxide leak', 'water heater CO leak', 'generator CO poisoning',
            'car exhaust poisoning', 'hotel carbon monoxide', 'apartment CO leak',
            'faulty heating system CO', 'blocked flue CO poisoning',
            
            # Legal context
            'carbon monoxide lawyer', 'CO poisoning attorney', 'carbon monoxide lawsuit',
            'CO detector failure lawsuit', 'landlord CO negligence', 'hotel CO poisoning lawsuit'
        ],
        
        'pesticide_exposure': [
            # Core terms
            'pesticide exposure', 'pesticide poisoning', 'chemical pesticide injury',
            'insecticide exposure', 'herbicide exposure', 'fungicide exposure',
            'agricultural chemical exposure', 'crop dusting exposure',
            
            # Specific pesticides
            'organophosphate exposure', 'glyphosate exposure', 'atrazine exposure',
            '2,4-D exposure', 'chlorpyrifos exposure', 'paraquat exposure',
            
            # Health effects
            'pesticide neurological damage', 'pesticide cancer', 'pesticide birth defects',
            'pesticide respiratory problems', 'pesticide skin problems',
            
            # Legal context
            'pesticide exposure lawyer', 'agricultural chemical attorney', 'pesticide poisoning lawsuit',
            'farm worker pesticide claim', 'pesticide drift lawsuit'
        ],
    },

    # 12. Professional Negligence
    'professional_negligence': {
        'legal_malpractice': [
            # Core terms
            'legal malpractice', 'attorney malpractice', 'lawyer malpractice',
            'attorney negligence', 'lawyer negligence', 'legal negligence',
            'legal professional negligence', 'law firm negligence',
            
            # Specific errors
            'missed statute of limitations', 'conflict of interest attorney',
            'inadequate representation', 'failure to file lawsuit', 'legal research negligence',
            'settlement negligence', 'trial preparation negligence', 'discovery negligence',
            
            # Legal context
            'legal malpractice lawyer', 'attorney malpractice attorney', 'lawyer negligence lawsuit',
            'legal malpractice claim', 'attorney malpractice suit', 'law firm lawsuit'
        ],
        
        'accounting_malpractice': [
            # Core terms
            'accounting malpractice', 'accountant negligence', 'CPA malpractice',
            'CPA negligence', 'accounting negligence', 'accounting error',
            'tax preparation negligence', 'audit negligence',
            
            # Specific errors
            'tax preparer error', 'accounting fraud', 'financial statement error',
            'tax return error', 'bookkeeping negligence', 'payroll error',
            'IRS penalty accountant error', 'missed tax deduction',
            
            # Legal context
            'accounting malpractice lawyer', 'CPA negligence attorney', 'accountant malpractice lawsuit',
            'tax preparer lawsuit', 'accounting negligence claim'
        ],
        
        'insurance_bad_faith': [
            # Core terms
            'insurance bad faith', 'insurance company bad faith', 'insurer bad faith',
            'insurance denial', 'wrongful denial insurance', 'insurance claim denial',
            'insurance dispute', 'insurance company negligence', 'insurance breach of contract',
            
            # Specific issues
            'unreasonable claim denial', 'delayed insurance payment', 'lowball settlement offer',
            'failure to investigate claim', 'insurance coverage dispute', 'policy interpretation dispute',
            'excess judgment insurance', 'failure to defend insurance',
            
            # Legal context
            'insurance bad faith lawyer', 'insurance denial attorney', 'bad faith insurance lawsuit',
            'insurance dispute lawyer', 'insurance coverage attorney', 'insurance claim lawyer'
        ],
    },

}