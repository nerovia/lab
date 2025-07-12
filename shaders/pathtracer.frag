#version 300 es

precision mediump float;

const float TOL = 1e-3;
const float PI = acos(-1.0);

#define CAMERA_FOV      	0.90
#define CAMERA_NEAR     	0.000001
#define CAMERA_FAR      	1000.0

struct Material {
    vec3 albedo;  // ambient color
    vec3 emissiv; // specular color
    float ke;      // emissiv factor
    float kd;      // diffuse factor
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
    bool has_hit;
    float hit_distance; // the distance to the closest instersection
    vec3 hit_normal;    // the normal vector of the intersected surface
    vec3 hit_position;  // the world position of the intersection
    vec3 hit_texture;     
    int hit_material;         // the object that was indersected
};


Material MATERIALS[4] = Material[](
    Material(
        vec3(1.0, 1.0, 1.0), // albedo color
        vec3(0), // emissiv color
        0.0,  // [ke] emissiv factor
        10.0,  // [kd] diffuse factor
        0.1,  // [kr] reflection factor
        0.0,  // [kt] transmission factor
        200.0, // shinyness coefficent
        1.2  // refraction index
    ),
    Material(
        vec3(0.7137, 0.4706, 0.9255), // albedo color
        vec3(0), // emissiv color
        0.0,  // [ke] emissiv factor
        0.1,  // [kd] diffuse factor
        0.1,  // [kr] reflection factor
        0.0,  // [kt] transmission factor
        200.0, // shinyness coefficent
        1.2  // refraction index
    ),
    Material(
        vec3(1.0, 0.0314, 0.9176), // albedo color
        vec3(0.9765, 0.9882, 0.902), // emissiv color
        1.0,  // [ke] emissiv factor
        1.0,  // [kd] diffuse factor
        0.1,  // [kr] reflection factor
        0.0,  // [kt] transmission factor
        200.0, // shinyness coefficent
        1.2  // refraction index
    ),
    Material(
        vec3(1.0, 1.0, 1.0), // albedo color
        vec3(0.9765, 0.9882, 0.902), // emissiv color
        1.0,  // [ke] emissiv factor
        1.0,  // [kd] diffuse factor
        0.1,  // [kr] reflection factor
        0.0,  // [kt] transmission factor
        200.0, // shinyness coefficent
        1.2  // refraction index
    )
);

const vec3 BACKGROUND = vec3(0.651, 0.8471, 0.898);
const float FOCAL_LENGTH = 10.0;

Plane PLANES[6] = Plane[6](
    Plane(vec3(-3, 0, 0), vec3(1, 0, 0), 1),
    Plane(vec3(2, 0, 0), vec3(-1, 0, 0), 1),
    Plane(vec3(0, 0, 10), vec3(0, 0, -1), 1),
    Plane(vec3(0, 0, -4), vec3(0, 0, -1), 1),
    Plane(vec3(0, -2, 0), vec3(0, 1, 0), 1),
    Plane(vec3(0, 2, 0), vec3(0, -1, 0), 3)
);

Sphere SPHERES[2] = Sphere[2](
    Sphere(vec3(0.0, 0.0, 1.8), .6, 2),
    Sphere(vec3(0.0, -1.2, 1.8), 0.8, 0)
);

Sphere LIGHT = Sphere(vec3(0, 1.5, 0), .05, -1);

in vec4 v_position;
uniform float u_time;
uniform vec2 u_resolution;
uniform vec2 u_mouse;
uniform sampler2D u_texture_0;
uniform vec3 u_camera;

out vec4 frag_color;

int seed;

int xorshift(in int value) {
    // Xorshift*32
    // Based on George Marsaglia's work: http://www.jstatsoft.org/v08/i14/paper
    value ^= value << 13;
    value ^= value >> 17;
    value ^= value << 5;
    return value;
}

float rand(inout int seed) {
    seed = xorshift(seed);
    // FIXME: This should have been a seed mapped from MIN..MAX to 0..1 instead
    return abs(fract(float(seed) / 3141.592653));
}


// highp float rand(vec2 co)
// {
//     highp float a = 12.9898;
//     highp float b = 78.233;
//     highp float c = 43758.5453;
//     highp float dt= dot(co.xy ,vec2(a,b));
//     highp float sn= mod(dt,3.14);
//     return fract(sin(sn) * c);
// }


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
    ray.hit_material = plane.material_id;
    ray.has_hit = true;

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
    ray.hit_material = sphere.material_id;
    ray.has_hit = true;
}


RayCast ray_cast(vec3 origin, vec3 direction) {
    // initialize raycast object
    RayCast ray;
    ray.origin = origin;
    ray.direction = normalize(direction);
    ray.hit_distance = 1e10;
    ray.has_hit = false;

    // test all objects in scene
    for (int i = 0; i < SPHERES.length(); i++)
        intersect_sphere(ray, SPHERES[i]);

    for (int i = 0; i < PLANES.length(); i++)
        intersect_plane(ray, PLANES[i]);

    return ray;
}


vec3 sample_hemisphere(vec3 n) {
    float u1 = rand(seed);
    float u2 = rand(seed);

    float r = sqrt(u1);
    float theta = 2.0 * PI * u2;

    // Sample in local tangent space (Y-up)
    vec3 localDir = vec3(r * cos(theta), sqrt(1.0 - u1), r * sin(theta));

    // Orthonormal basis: Tangent, Bitangent, Normal
    vec3 tangent = normalize(cross(abs(n.y) < 0.999 ? vec3(0,1,0) : vec3(1,0,0), n));
    vec3 bitangent = cross(n, tangent);

    // Transform to world space
    return localDir.x * tangent + localDir.y * n + localDir.z * bitangent;
}


vec3 ray_trace(vec3 origin, vec3 direction) {
    RayCast ray = ray_cast(origin, direction);

    if (!ray.has_hit)
        return BACKGROUND;
    
    Material m = MATERIALS[ray.hit_material];
    vec3 color = 0.2 * m.albedo;
    vec3 light = LIGHT.center;

    vec3 n = ray.hit_normal;
    vec3 l = normalize(light - ray.hit_position);
    vec3 r = reflect(-l, n); // flip to incoming direction
    vec3 v = -ray.direction; // flip to outcoming direction
        
    float d = max(0.0, dot(n, l));
    float s = max(0.0, dot(r, v));

    RayCast shadow_ray = ray_cast(ray.hit_position, l);
    if (shadow_ray.hit_distance > distance(light, ray.hit_position)) {
        color += m.kd * d * m.albedo;
        color += 0.4 * pow(s, 4.0) * vec3(1);
    }

    return color;
}

vec3 path_trace(vec3 origin, vec3 direction) {
    const int N = 4;

    vec3 color = vec3(0.0);
    vec3 weight = vec3(1.0);

    for (int i = 0; i < N; ++i) {
        RayCast ray = ray_cast(origin, direction);
        Material m = MATERIALS[ray.hit_material];

        if (!ray.has_hit) {
            color = weight * BACKGROUND;
            break;
        }

        if (m.ke > 0.0) {
            color = weight * m.emissiv * m.ke;
            
        }

        origin = ray.hit_position;
        direction = sample_hemisphere(ray.hit_normal);

        vec3 brdf = m.albedo / PI;
        float cos_theta = max(0.0, dot(direction, ray.hit_normal));

        weight *= brdf * cos_theta * m.kd;
        
        float p = max(weight.r, max(weight.g, weight.b));
        weight /= p;
    }

    return color;
}


void animate(float t) {
    //PLANES[5].position.y = cos(t) + 2.0;
    MATERIALS[3].ke = 0.5 * sin(t) + 0.5;
    //LIGHT.center = vec3(0);
    //LIGHT.center.xz = 1.0 * vec2(sin(2.0*t), cos(2.0*t));
    //SPHERES[0].center.xz = vec2(sin(t), cos(t)) * vec2(1.1, 01.5);
    //SPHERES[1].center.x = -0.5 * sin(t) + 1.0;
}


void main() {
    
    vec2 mouse = u_mouse / u_resolution;
    float aspect = 1.0 / max(u_resolution.x, u_resolution.y);
    vec2 coord = gl_FragCoord.xy;
    seed = int(coord.x) * int(coord.y);
    

    vec3 cam_position = u_camera * .2;
    vec3 cam_lookat = vec3(0, 0, 0);
    vec3 cam_up = vec3(0, 1, 0);
    float fov = 0.5 * PI;
    float focal_length = 1.0; 

    float scale = tan(fov * 0.5);
    vec3 forward = normalize(cam_lookat - cam_position);
    vec3 right = normalize(cross(forward, cam_up));
    vec3 up = cross(right, forward);

    animate(u_time);

    vec2 uv = 2.0 * coord * aspect - vec2(1.0);
    vec3 origin = cam_position; 
    vec3 direction = normalize(
        forward * focal_length + 
        right * uv.x * scale + 
        up * uv.y * scale
    );

    const int N = 32;
    vec3 color_acc = vec3(0);
    for (int i = 0; i < N; ++i) {
        color_acc += path_trace(origin, direction);
    }

    frag_color = vec4(color_acc / float(N), 1);

    // const int S = 5;     // Number of subsamples in x and y direction
    // const int s = S / 2; // Index offset from pixel center
    // const float d = 0.0; // Distance offset from pixel center
    // vec3 color_acc = vec3(0);

    // for (int i = 0; i < S; ++i) {
    //     for (int j = 0; j < S; ++j) {
    //         float dx = float(i - s) * d;
    //         float dy = float(j - s) * d;

    //         vec2 uv = 2.0 * (coord + vec2(dx, dy)) * aspect - vec2(1.0);
    //         vec3 origin = cam_position; 
    //         vec3 direction = normalize(
    //             forward * focal_length + 
    //             right * uv.x * scale + 
    //             up * uv.y * scale
    //         );
    //         color_acc += path_trace(origin, direction);
    //     }


    // }

    // frag_color = vec4(color_acc / float(S*S), 1);
}
