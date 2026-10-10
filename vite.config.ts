import { defineConfig } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";

export default defineConfig({
    plugins: [
        svelte({
            compilerOptions: {
                customElement: true,
                css: "injected",
            }
        })
    ]
})

// export default defineConfig({
//     plugins: [
//         svelte({
//             compilerOptions: {
//                 css: "injected",
//             }
//         })
//     ],
//     build: {
//         lib: {
//             entry: svelteFiles,
//             name: "PySvelte",
//             formats: ["iife"],
//             fileName: (format, entryName) => `${entryName}.${format}.js`
//         }
//     }
// })