import { Html, Head, Main, NextScript } from 'next/document';

export default function Document() {
  return (
    <Html lang="en">
      <Head />
      <head><title>SkinSafe</title></head>
      <body className="h-screen w-screen bg-gradient-to-br bg-no-repeat from-purple-900 to-blue-900">
        <Main />
        <NextScript />
      </body>
    </Html>
  );
}
