# Dream Imagery → Visual Element Mapping

## Mood → Color scheme

| mood value | Mood | Primary | Secondary | Background |
|---------|------|------|------|------|
| anxious | anxiety/fear | #2D1B69 deep purple | #1A1A2E dark blue | dark gradient |
| peaceful | calm/pleasant | #F4D35E warm yellow | #83C5BE soft green | light gradient |
| sad | sadness/loss | #4A6FA5 slate blue | #2D3142 dark gray | cool gradient |
| surreal | fantastical/absurd | #FF006E neon pink | #8338EC electric purple | dark + neon accents |
| exciting | excitement/thrill | #FF6B35 orange-red | #FFD700 gold | warm gradient |
| nostalgic | nostalgia/warmth | #DDA15E amber | #BC6C25 warm brown | soft-light gradient |

## Imagery → Visual elements

Each visual element corresponds to a drawing module in p5.js.

### Natural elements

| Imagery keywords | visual_element value | p5.js rendering |
|-----------|-------------------|------------|
| water, sea, river, lake, swimming | water_ripple | sinusoidal ripples spreading upward from the bottom |
| rain | rain_drops | thin-line particles falling from above |
| fire, burning | fire_particles | orange-red particles drifting upward |
| wind, storm | wind_lines | horizontal flowing curves |
| starry sky, night sky | starfield | small randomly twinkling points of light |
| moon | moon_glow | circular halo, slow pulsing |
| sun, light | sun_rays | radial beams |
| forest, trees | tree_silhouettes | tree silhouettes along the bottom |
| flowers, garden | floating_petals | slowly drifting petal shapes |

### Spaces / architecture

| Imagery keywords | visual_element value | p5.js rendering |
|-----------|-------------------|------------|
| high-rise, skyscraper, tower | building | architectural outlines built from geometric lines |
| room, indoors | room_frame | room frame made of perspective lines |
| door | door_shape | central door outline, possibly opening/closing |
| stairs, steps | stairs | ascending step lines |
| maze, corridor | maze_lines | randomly generated path lines |
| bridge | bridge_arc | arched bridge outline |

### Actions / states

| Imagery keywords | visual_element value | p5.js rendering |
|-----------|-------------------|------------|
| falling, dropping | falling_particles | particles accelerating downward |
| flying, floating | rising_particles | particles slowly rising |
| chase, escape | speed_lines | high-speed horizontal lines |
| trapped, enclosed | cage_lines | enclosing lines gradually contracting |
| lost | scattered_dots | randomly drifting points of light |

### People / creatures

| Imagery keywords | visual_element value | p5.js rendering |
|-----------|-------------------|------------|
| person, figure | human_silhouette | abstract human silhouette, fading in and out |
| crowd | crowd_dots | many small dots gathering and scattering |
| snake | snake_curve | slow S-shaped curve slithering |
| cat/dog/animal | animal_shape | simple sketched animal outline |
| bird/flying creature | bird_flight | V-shaped outline crossing the frame |
| fish/aquatic creature | fish_swim | oval shapes weaving through water ripples |

### Atmosphere modifiers

| Imagery keywords | visual_element value | p5.js rendering |
|-----------|-------------------|------------|
| darkness, can't see clearly | dark_bg | overall low brightness + blurred light patches |
| blurry, hazy | blur_lights | Gaussian-blurred points of light |
| flickering, unstable | flicker_effect | random fluctuation of overall frame brightness |
| spinning, dizzy | spiral_motion | particles in spiral motion |
| quiet, empty | minimal_space | large empty areas + minimal elements |

## Mapping rules

1. Extract every recognizable image from the dream description
2. Each image maps to one visual_element
3. The visual_elements array holds at most 5 elements (to keep the scene from getting too busy)
4. Prefer imagery related to the main plot
5. Include at least 1 atmosphere modifier element
6. Take the mood from the strongest emotion in the dream; the color_scheme corresponds to the mood
