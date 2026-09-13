const djangoApiUrl = process.env.DJANGO_ADMIN_API_URL ?? "http://127.0.0.1:8000/api";

export async function POST(request: Request) {
  const response = await fetch(`${djangoApiUrl}/scanner/scan/`, { method: "POST", headers: {"Content-Type":"application/json"}, body: await request.text(), cache: "no-store" });
  return new Response(await response.text(), { status: response.status, headers: {"Content-Type":"application/json"} });
}
