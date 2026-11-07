'use server';
import { apiClient } from "@/lib/api";
import { LoginResponse } from "@/lib/types";
import { setToken, removeToken } from "@/lib/auth";
import { redirect } from "next/navigation";

export async function createAccountAction(
    prevState: { success: boolean, error: string, redirectTo?: string } | null,
    formData: FormData
) {
    try {
        const username = formData.get('username');
        const email = formData.get('email');
        const password = formData.get('password');

        const data = {
            username: username,
            email: email,
            password: password
        }

        await apiClient('/api/v1/users', {
            method: "POST",
            body: JSON.stringify(data)
        })

        return { success: true, error: '', redirectTo: '/login' };
    } catch (error) {
        if (error instanceof Error) {
            return { success: false, error: error.message }
        }

        return { success: false, error: "Error creating account" }
    }

}

export async function loginAction(
    prevState: { success: boolean, error: string, redirectTo?: string, token?: string } | null,
    formData: FormData
) {
    try {
        const email = formData.get('email');
        const password = formData.get('password');

        const data = {
            email: email,
            password: password
        }

        const response = await apiClient<LoginResponse>('/api/v1/auth/token', {
            method: "POST",
            body: JSON.stringify(data)
        })

        await setToken(response.access_token);

        return { success: true, error: '', redirectTo: '/dashboard', token: response.access_token };
    } catch (error) {
        if (error instanceof Error) {
            return { success: false, error: error.message }
        }

        return { success: false, error: "Error loggin into account" }
    }
}

export async function logoutAction() {
    await removeToken();
    redirect('/login')
}