
const API_URL = process.env.NEXT_PUBLIC_API_URL as string;

export function getApiUrl() {
    return API_URL;
}

interface FetchOptions extends RequestInit {
    token?: string;
    cache?: "force-cache" | "no-store";
    next?: {
        revalidate?: false | 0 | number;
        tags?: string[]
    }
}

export async function apiClient<T>(
    endpoint: string,
    options: FetchOptions = {}
): Promise<T> {

    const { token, ...fetchOptions } = options;
    const headers: Record<string, string> = {
        ...(fetchOptions.headers as Record<string, string>)
    }

    if (token) {
        headers['Authorization'] = `Bearer ${token}`;
    }

    if (!(fetchOptions.body instanceof FormData)) {
        headers["Content-Type"] = "application/json"
    }

    const response = await fetch(`${API_URL}${endpoint}`, {
        ...fetchOptions,
        headers
    })

    if (!response.ok) {
        const error = await response.json().catch(() => ({
            detail: "HTTP Error: " + response.status,
        }));

        const message = Array.isArray(error.detail)
            ? error.detail.map((item: { msg: string }) => item.msg).join("\n")
            : error.detail;

        throw new Error(message || "HTTP Error: " + response.status);

    }

    if (response.status == 204) {
        return undefined as T;
    }

    return response.json();

}