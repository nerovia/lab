#version 300 es

precision mediump float;

const float TOL = 1e-3;

struct Material {
    vec3 ambient;  // ambient color
    vec3 diffuse;  // diffuse color
    vec3 specular; // specular color
    float ka;      // ambient factor
    float kd;      // diffuse factor
    float ks;      // specular factor
    float kr;      // reflection factor
    float kt;      // transmission factor
    float n;       // shinyness coefficent
    float eta;     // refraction index
};

struct Plane {
    vec3 position;
    vec3 normal;
    int material_id;
};

struct Sphere {
    vec3 center;
    float radius;
    int material_id;
};



struct RayCast {
    vec3 origin;        // the origin of the ray
    vec3 direction;     // the nomalized direction of the ray
    float hit_distance; // the distance to the closest instersection
    vec3 hit_normal;    // the normal vector of the intersected surface
    vec3 hit_position;  // the world position of the intersection
    vec3 hit_texture;     
    int hit_id;         // the object that was indersected
    float weight;
};


Material MATERIALS[4] = Material[4](
    Material(
        vec3(1, 0, 0), // ambient color
        vec3(1.0, 0.3216, 0.3216), // diffuse color
        vec3(1, 1, 1), // specular color
        0.3,  // [ka] ambient factor
        0.7,  // [kd] diffuse factor
        0.7,  // [ks] specular factor
        0.1,  // [kr] reflection factor
        0.0,  // [kt] transmission factor
        200.0, // shinyness coefficent
        1.2  // refraction index
    ),
    Material(
        vec3(0.1922, 0.1922, 0.1922), // ambient color
        vec3(0.149, 0.3569, 0.5255), // diffuse color
        vec3(1.0, 1.0, 1.0), // specular color
        0.3,  // [ka] ambient factor
        0.2,  // [kd] diffuse factor
        0.3,  // [ks] specular factor
        0.4,  // [kr] reflection factor
        0.5,  // [kt] transmission factor
        20.0, // shinyness coefficent
        1.05  // refraction index
    ),
    Material(
        vec3(0.4706, 0.9255, 0.7804), // ambient color
        vec3(0.4706, 0.9255, 0.7804), // diffuse color
        vec3(1, 1, 1), // specular color
        0.3,  // [ka] ambient factor
        0.7,  // [kd] diffuse factor
        0.1,  // [ks] specular factor
        0.0,  // [kr] reflection factor
        0.0,  // [kt] transmission factor
        200.0, // shinyness coefficent
        1.2  // refraction index
    ),
    Material(
        vec3(0.5569, 0.5569, 0.5569), // ambient color
        vec3(0.6588, 0.7922, 0.851), // diffuse color
        vec3(1, 1, 1), // specular color
        0.0,  // [ka] ambient factor
        0.1,  // [kd] diffuse factor
        0.0,  // [ks] specular factor
        0.8,  // [kr] reflection factor
        0.0,  // [kt] transmission factor
        200.0, // shinyness coefficent
        1.2  // refraction index
    )
);

const vec3 BACKGROUND = vec3(0.651, 0.8471, 0.898);
const float FOCAL_LENGTH = 10.0;

Plane PLANES[6] = Plane[6](
    Plane(vec3(-2, 0, 0), vec3(1, 0, 0), 2),
    Plane(vec3(2, 0, 0), vec3(-1, 0, 0), 2),
    Plane(vec3(0, 0, 4), normalize(vec3(0.2, 0, -1)), 3),
    Plane(vec3(0, 0, -8), vec3(0, 0, -1), 3),
    Plane(vec3(0, -2, 0), vec3(0, 1, 0), 2),
    Plane(vec3(0, 2, 0), vec3(0, -1, 0), 2)
);

Sphere SPHERES[2] = Sphere[2](
    Sphere(vec3(0.5, 0, 0), .3, 0),
    Sphere(vec3(-0.3, -1.2, 0), 0.8, 1)
);

Sphere LIGHT = Sphere(vec3(0, 1.5, 0), .05, -1);

in vec4 v_position;
uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform sampler2D u_texture_0;

out vec4 frag_color;



float rand (vec2 st) {
    return fract(sin(dot(st.xy,
                         vec2(12.9898,78.233)))*
        43758.5453123);
}


void intersect_plane(inout RayCast ray, in Plane plane) {

    vec3 o = ray.origin;
    vec3 u = ray.direction;
    vec3 p = plane.position;
    vec3 n = plane.normal;

    vec3 op = p - o;
    float un = dot(u, n);

    if (un == 0.0)
        return;

    float d = dot(op, n) / un;

    // check if the ray hit something closer
    if (d < TOL || d > ray.hit_distance)
        return;
    
    // determine intersection point and surface normal
    vec3 q = o + d * u;


    // update raycast hit
    ray.hit_distance = d;
    ray.hit_position = q;
    ray.hit_normal = n;
    ray.hit_id = plane.material_id;

    // vec3 up = vec3(0, 1, 0); // since all n are on xz-plane right now
    // vec3 tangent = cross(up, n);
    // mat3 basis = mat3(tangent, up, n);
    // vec2 uv = (transpose(basis) * q).st;

    // ray.hit_texture = texture(u_texture_0, fract(uv), 0.0).rgb;

}

void intersect_sphere(inout RayCast ray, in Sphere sphere) {

    // parameters
    vec3 o = ray.origin;
    vec3 u = ray.direction;
    vec3 p = sphere.center;
    float r = sphere.radius;

    vec3 op = o - p;
    float b = dot(u, (op));
    float c = dot(op, op) - (r * r); 

    // determine if intersection exists
    float det = b * b - c;
    if (det < 0.0)
        return;
        
    // determine intersection distance
    float detSqrt = sqrt(det);
    float d1 = -b + detSqrt;
    float d2 = -b - detSqrt;
    float d = min(d1, d2);

    // check if the ray hit something closer
    if (d < TOL || d > ray.hit_distance)
        return;
    
    // determine intersection point and surface normal
    vec3 q = o + d * u;
    vec3 n = normalize(q - p);

    // update raycast hit
    ray.hit_distance = d;
    ray.hit_position = q;
    ray.hit_normal = n;
    ray.hit_id = sphere.material_id;
}


RayCast ray_cast(vec3 origin, vec3 direction) {
    // initialize raycast object
    RayCast ray;
    ray.origin = origin;
    ray.direction = normalize(direction);
    ray.hit_distance = 1e10;
    ray.hit_id = -1;

    // test all objects in scene
    for (int i = 0; i < SPHERES.length(); i++)
        intersect_sphere(ray, SPHERES[i]);

    for (int i = 0; i < PLANES.length(); i++)
        intersect_plane(ray, PLANES[i]);

    return ray;
}


vec3 shade(in RayCast ray) {
    if (ray.hit_id < 0)
        return BACKGROUND;
    
    Material m = MATERIALS[ray.hit_id];
    vec3 color = m.ka * m.ambient ;
    vec3 light = LIGHT.center;

    vec3 n = ray.hit_normal;
    vec3 l = normalize(light - ray.hit_position);
    vec3 r = reflect(-l, n); // flip to incoming direction
    vec3 v = -ray.direction; // flip to outcoming direction
        
    float d = max(0.0, dot(n, l));
    float s = max(0.0, dot(r, v));

    RayCast shadow_ray = ray_cast(ray.hit_position, l);
    if (shadow_ray.hit_distance > distance(light, ray.hit_position)) {

        color += m.kd * d * m.diffuse;
        color += m.ks * pow(s, m.n) * m.specular;
    }

    return color;
}

vec3 trace(RayCast ray) {
    const int K = 8;  // 2^N Depth 

    Material m;
    RayCast rays[K*2];
    rays[1] = ray;
    rays[1].weight = 1.0;

    vec3 color_acc = vec3(0.0, 0.0, 0.0);

    // Cast rays
    for (int i = 1; i < K; i++) {

        ray = rays[i];
        m = MATERIALS[ray.hit_id];

        int r = i*2;
        int t = i*2+1;

        if (ray.hit_id >= 0) {
            vec3 refl = reflect(ray.direction, ray.hit_normal);
            rays[r] = ray_cast(ray.hit_position, refl);
            rays[r].weight = ray.weight * m.kr;
            vec3 refr = refract(ray.direction, ray.hit_normal, m.eta);
            rays[t] = ray_cast(ray.hit_position, refr);
            rays[t].weight = ray.weight * m.kt;
        }
        else {
            rays[r].hit_id = -1;
            rays[t].hit_id = -1;
        }
    }

    // Accumulate rays
    vec3 color = shade(rays[1]);
    for (int i = 1; i < K; i++) {
        int r = i*2;
        int t = i*2+1;
        color += rays[r].weight * shade(rays[r]);
        color += rays[t].weight * shade(rays[t]);
    }


    return color;

}



void main() {
    
    vec2 mouse = u_mouse / u_resolution;
    vec3 aspect = vec3(u_resolution / max(u_resolution.x, u_resolution.y), 1);
    vec3 pos = v_position.xyz * aspect * 2.0;

    float t = u_time * 1.0;
    // t = mouse.x * 4.0 * 3.14;
    LIGHT.center = vec3(0);
    LIGHT.center.xz = 1.0 * vec2(sin(2.0*t), cos(2.0*t));
    SPHERES[0].center.xz = vec2(sin(t), cos(t)) * vec2(1.1, 01.5);
    //SPHERES[1].center.x = -0.5 * sin(t) + 1.0;

    vec3 light = LIGHT.center;

    vec3 f = vec3(0, -0.5, -5.0);

    // RayCast ray = ray_cast(vec3(pos.xy, -10), vec3(0, 0, 1));
    RayCast ray = ray_cast(f, pos - f);


    vec3 color = trace(ray);
    frag_color = vec4(color , 1);
    

    // intersect_sphere(ray, LIGHT);
    // if (ray.hit_id == 2) {
    //     frag_color = vec4(1, 1, 0, 1);
    // }

    
    // else
    //     frag_color = vec4(0, 0, 0, 1);
}
