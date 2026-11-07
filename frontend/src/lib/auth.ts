import { cookies } from "next/headers";
import { apiClient } from "./api";
import { User } from "./types";

const COOKIE_NAME = 'my_api_session';

export async function getToken(): Promise<string | undefined> {
    const cookieStore = await cookies();
    return cookieStore.get(COOKIE_NAME)?.value
}

export async function setToken(token: string) {
    const cookieStore = await cookies();
    cookieStore.set(COOKIE_NAME, token, {
        httpOnly: true,
        maxAge: 60 * 30,
        path: '/',
        sameSite: true,
        secure: process.env.NODE_ENV === 'production'
    });
}

export async function removeToken() {
    const cookieStore = await cookies();
    cookieStore.delete(COOKIE_NAME);
}

export async function getUser(): Promise<User | null> {
    try {
        const token = await getToken();
        if (!token) {
            return null;
        }

        const user = await apiClient<User>('/api/v1/users/me', {
            method: 'GET',
            token: token
        })

        console.log(user)
        return user

    } catch (error) {
        console.log(error);
        return null;
    }
}