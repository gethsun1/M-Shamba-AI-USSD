/// <reference types="vite/client" />

interface ImportMetaEnv {
  readonly VITE_USSD_API_URL: string;
  readonly VITE_USSD_SERVICE_CODE: string;
  readonly VITE_USSD_PHONE_NUMBER: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}
