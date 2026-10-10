import { build } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { resolve } from "path";
import fs from "fs";

const pkgDir = resolve(import.meta.dirname, "pkg")
const svelteFiles = fs.readdirSync(pkgDir)
    .filter((file: string) => file.endsWith(".svelte"))
    .map((file: string) => resolve(pkgDir, file));
// const buildFiles = svelteFiles
//     .map((file: string) => file.split("/")[-1].replace(".svelte", ""));

// console.log(svelteFiles)
svelteFiles.forEach((file) => {
    let buildFile = (file.split("/").at(-1) ?? "").replace(".svelte", "");

    return build({
        configFile: false,
        build: {
            lib: {
                entry: file,
                name: buildFile,
                formats: ["iife"],
                fileName: (format: string, entryName: string) => `${entryName}.${format}.js`
            },
        },
        plugins: [
            svelte({
                compilerOptions: {
                    customElement: true,
                    css: "injected",
                }
            })
        ]
    })
});