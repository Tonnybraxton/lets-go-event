const djangoApiUrl = process.env.DJANGO_ADMIN_API_URL ?? "http://127.0.0.1:8000/api";

export async function GET(_request: Request, { params }: { params: Promise<{ reference: string }> }) {
  const { reference } = await params;
  const response = await fetch(`${djangoApiUrl}/orders/${encodeURIComponent(reference)}/`, {
    cache: "no-store",
    headers: { Accept: "application/json" },
  });
  return new Response(await response.text(), {
    status: response.status,
    headers: { "Content-Type": "application/json", "Cache-Control": "no-store" },
  });
}

