<script lang="ts">
    import { line } from "d3-shape";

    export let data: [number, number][] = [[0, 0], [50, 50], [100, 100], [200, 200]]
    export let title;

    const lineGenerator = line()
        .x((d) => d[0])
        .y((d) => d[1])
</script>

<div>
    <h1>{title}</h1>
    <svg width=800 height=600>
        <path 
            d={lineGenerator(data)}
            stroke="#00ffee"
            stroke-width="1.5"
            fill="none"
        />
    </svg>
</div>