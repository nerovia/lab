#version 300 es

precision mediump float;

// This shader is based on (https://www.shadertoy.com/view/3tyXWw)

// Constants
const float PI = acos(-1.);
const int ITERATIONS = 32;
const float THICKNESS = 0.02;

// Varyings
in vec4 v_position;
in vec2 v_texcoord;
out vec4 frag_color;

// Uniforms
uniform vec2 u_resolution;
uniform vec2 u_mouse;

// Parameters
vec3 wythoff_symbol = vec3(3, 3, 3);

// Signed distance from line
float sd_line(vec2 v, vec3 l) { return dot(v, l.xy) - l.z; }

// Signed distance from line segment
float sd_segment(vec2 v, vec2 p, vec2 q) {
    vec2 vp = v-p;
    vec2 qp = q-p;
    float h = clamp( dot(vp,qp)/dot(qp,qp), 0.0, 1.0 );
    return length( vp - qp*h );
}

// Relfect on triangle edges
vec2 involution(vec2 uv, vec3 edges[3], out float parity) {
    
    // we try to get the uv position back into the fundametal domain, by reflecting it a bunch of times
    
    parity = 1.0;
    for (int i = 0; i < 32; ++i) {

        // reflection on j-th edge
        int j = 0;
        while (j < 3) {
            float d = sd_line(uv, edges[j]); // distance to the j-th edge
            
            // if the point is on the wrong side of the edge (not near the triangle) 
            if (d > 0.) { 
                // reflect
                uv -= edges[j].xy * d * 2.0; // we subtract because, the normal vectors point outwards of the triangle
                parity *= -1.0;
                break;
            }
            ++j; // count how many times the point is on the correct side
        }

        if (j == 3) // if the point is whitin the fundamental domain
            break;
    }

    return uv;
}

void main() {

    // position
    vec2 aspect = u_resolution / max(u_resolution.x, u_resolution.y) * 4.0;
    vec2 pos = v_position.xy * aspect;
    vec2 uv = pos;
    vec2 mouse = ((u_mouse.xy / u_resolution.xy)*2.0 -vec2(1.0)) * aspect;

    // get triangle angles from wythoff wythoff_symbol
    vec3 angles = vec3(PI) / wythoff_symbol;
    vec3 sins = sin(angles);

    // the wythoff wythoff_symbol describes a right triangle
    // get the side length, where c=1
    float a = sins.x / sins.z;
    float b = sins.y / sins.z;
    float c = 1.0;

    // corner positions
    vec2 A = vec2(0, 0);
    vec2 B = vec2(1, 0);
    vec2 C = vec2(cos(angles.x), sin(angles.y)) * b;
    
    // triangle edge planes defined by a (orthogonal) normal vector
    // the normal vector is described by the xy components.
    // the z component describes the distance of the plane from the origin.
    float sinzx = sin(angles.z + angles.x);
    vec3 edges[3];
    edges[0] = vec3(-sin(angles.x), cos(angles.x), 0);        // orthogonal vector on side b
    edges[1] = vec3(0., -1., 0);                             // orthogonal vector on side c
    edges[2] = vec3(sinzx, -cos(angles.z + angles.x), sinzx); // orthogonal vector on side a 

    float parity;
    vec2 genpoint = involution(mouse, edges, parity);
    uv = involution(uv, edges, parity);

    float sides[3];
    float linedist = 1e6;

    for (int k = 0; k < 3; ++k) {
        vec2 gk = edges[k].xy * (dot(genpoint, edges[k].xy) - edges[k].z);
        vec2 ngk = normalize(gk).yx * vec2(-1, 1);
        sides[k] = dot(uv - genpoint, ngk); // distance to separator
        linedist = min(linedist, sd_segment(uv, genpoint, genpoint-gk));
    }

    int poly;
    if (sides[1] < 0.0 && sides[2] > 0.0)
        poly = 0;
    else if(sides[2] < 0.0 && sides[0] > 0.0)
        poly = 1;
    else
        poly = 2;


    frag_color = vec4(1);

    // Color polygons
    frag_color.rgb = poly == 0 ? vec3(0.9725, 0.8157, 0.1137) : (poly == 1 ? vec3(0.8588, 0.5882, 0.9686) : vec3(0.5216, 0.9765, 0.9529));

    // Color parity
    frag_color.rgb = mix(frag_color.rgb, vec3(0.6275, 0.2078, 0.2078), 0.3 * step(0.0, parity));

    // Color edges
    frag_color.rgb = mix(frag_color.rgb, vec3(1), 1.0-step(THICKNESS, linedist));

    // Color vertices
    frag_color.rgb = mix(frag_color.rgb, vec3(0), 1.0-step(THICKNESS, distance(uv, genpoint)));
}
