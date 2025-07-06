SCENE: object
LIGHTS: list
CAMERA: object
AMBIENT_LIGHT: object
BACKGROUND_LIGHT: object
MAX_DEPTH: int
MIN_WEIGHT: float


def fragment(position):
    direction = CAMERA.position - position
    ray = SCENE.cast_ray(origin=CAMERA.position, direction=direction)
    color = trace(ray)
    return color


def trace(ray, weight=1, depth=0):
    color = shade(ray)
    
    if ray.hit:
        object = ray.hit.object
        (ka, ke, kd, ks, kr, kt, n) = object.material
        {kr, kt} = object.material
        
        if depth < MAX_DEPTH and weight > MIN_WEIGHT:
            if object.is_reflective:
                refl = ray.hit.reflect()
                color += kr * trace(refl, weight * kr, depth+1)
                
            if object.is_transmissive:
                refr = ray.hit.refract()
                color += kt * trace(refr, weight * kt, depth+1)
    
    return color


def shade(ray):
    if not ray.hit:
        return BACKGROUND_LIGHT
    
    position = ray.hit.position
    object = ray.hit.object
    (ka, ke, kd, ks, kr, kt, n) = object.material 

    color = ke + ka * AMBIENT_LIGHT
    
    for light in LIGHTS:
        vecV = -ray.direction
        vecN = ray.hit.normal
        vecL = light.position - position
        shadow_ray = SCENE.cast_ray(origin=position, direction=vecL)
        
        if shadow_ray.length >= vecL.length:
            vecR = reflect(vecL, vecN)
            color += kd * light.intensity * max(0, dot(vecL, vecN))
            color += ks * light.intensity * max(0, dot(vecR, vecV))**n
            
    return color
