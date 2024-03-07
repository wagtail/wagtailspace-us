import inject from "@rollup/plugin-inject"
import scss from 'rollup-plugin-scss'
import copy from 'rollup-plugin-copy-assets'

const path = require('path');

const source = path.join('./wagtailspace', './static_src');
const destination = path.join('./wagtailspace', './static');


import { defineConfig } from 'vite';

process.env['NODE_ENV'] = 'development';

export default defineConfig({
    build: {
        lib: {
            entry: path.join(source, 'js', 'main.js'),
            name: 'main',
            fileName: '[name]'
        },
        outDir: path.join(destination, 'bundles'),
    },
    plugins: [
        inject({
            $: 'jquery',
            jQuery: "jquery"
        }),
        scss(
            ({ fileName: "main.css" })
        ),
        copy({

            assets: [
                "../images"
            ]
        })
    ],
})
