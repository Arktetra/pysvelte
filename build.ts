import { build } from "vite";
import { svelte } from "@sveltejs/vite-plugin-svelte";
import { resolve } from "path";
import fs from "fs";

const pkgDir = resolve(import.meta.dirname, "pkg");
const distDir = resolve(import.meta.dirname, "dist");
if (!fs.existsSync(distDir)) fs.mkdirSync(distDir);

const svelteFiles = fs.readdirSync(pkgDir)
    .filter((file: string) => file.endsWith(".svelte"));

svelteFiles.forEach((fileName) => {
    let baseName = fileName.replace(".svelte", "");
    
    // 1. Create a temporary JS file that exports both the component AND mount
    const tempEntryPath = resolve(pkgDir, `__entry_${baseName}.js`);
    const entryContent = `
        export { default } from "./${fileName}";
        export { mount } from "svelte";
    `;
    fs.writeFileSync(tempEntryPath, entryContent);

    build({
        configFile: false,
        build: {
            lib: {
                entry: tempEntryPath, // 2. Point Vite to the entry file instead
                name: baseName,
                formats: ["es"],
                fileName: (format: string) => `${baseName}.${format}.js`
            },
            rollupOptions: {
                external: [], // Packages Svelte entirely inside the bundle
            }
        },
        plugins: [
            svelte({ compilerOptions: { css: "injected" } })
        ]
    }).then(() => {
        // 3. Clean up the temporary entry file after the build completes
        if (fs.existsSync(tempEntryPath)) fs.unlinkSync(tempEntryPath);
    });
});
