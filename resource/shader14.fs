#version 330 core
out vec4 FragColor;

in vec2 TexCoord;

uniform sampler2D texture1; // GL_TEXTURE0
uniform sampler2D texture2; // GL_TEXTURE1

void main() {
    FragColor = mix(texture(texture1, TexCoord) , texture(texture2, TexCoord), 0.2);
    // FragColor = texture(texture1, TexCoord);
    // FragColor = texture(texture2, TexCoord);
    // FragColor = vec4(1, 0,0,0);
}


