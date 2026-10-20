import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  allowedDevOrigins: ["127.0.0.1"],
  images: {
    // The Django catalogue serves local media during development. Next.js blocks
    // private-network image origins unless this is explicitly enabled.
    dangerouslyAllowLocalIP: true,
    remotePatterns: [
      { protocol: "https", hostname: "images.unsplash.com" },
      { protocol: "https", hostname: "lipatix.com" },
      { protocol: "https", hostname: "tikohub.com" },
      { protocol: "https", hostname: "images.squarespace-cdn.com" },
      { protocol: "https", hostname: "sportanddev.org" },
      { protocol: "https", hostname: "k24.digital" },
      { protocol: "https", hostname: "madfun-assets.s3.af-south-1.amazonaws.com" },
      { protocol: "https", hostname: "gusiifest.com" },
      { protocol: "http", hostname: "127.0.0.1", port: "8000", pathname: "/media/**" },
      { protocol: "http", hostname: "localhost", port: "8000", pathname: "/media/**" },
    ],
  },
};

export default nextConfig;

