import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// Load environment variables
import dotenv from 'dotenv'
dotenv.config()

export default defineConfig({
  plugins: [react()],
  define: {
    'import.meta.env.VITE_USSD_API_URL': JSON.stringify(process.env.VITE_USSD_API_URL),
    'import.meta.env.VITE_USSD_SERVICE_CODE': JSON.stringify(process.env.VITE_USSD_SERVICE_CODE),
    'import.meta.env.VITE_USSD_PHONE_NUMBER': JSON.stringify(process.env.VITE_USSD_PHONE_NUMBER),
  },
})
