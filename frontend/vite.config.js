import fs from 'node:fs'
import path from 'node:path'
import { fileURLToPath } from 'node:url'

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const rootDir = fileURLToPath(new URL('.', import.meta.url))
const distDir = path.resolve(rootDir, 'dist')

const copy404Plugin = () => ({
  name: 'copy-404',
  closeBundle() {
    const indexPath = path.join(distDir, 'index.html')
    const notFoundPath = path.join(distDir, '404.html')
    if (fs.existsSync(indexPath)) {
      fs.copyFileSync(indexPath, notFoundPath)
    }
  },
})

// https://vitejs.dev/config/
export default defineConfig({
  base: '/',
  plugins: [react(), copy404Plugin()],
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
