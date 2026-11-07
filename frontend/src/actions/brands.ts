'use server'
import { apiClient } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Brand } from "@/lib/types";
import { revalidatePath } from "next/cache";

export async function createBrand(formData: FormData) {
    try {
        const name = formData.get('name');

        const token = await getToken();

        if (!token) {
            return { success: false, error: 'Error al crear marca' }
        }

        const data = {
            name: name
        }

        const response = await apiClient<Brand>('/api/v1/brands/', {
            method: 'POST',
            body: JSON.stringify(data),
            token: token
        })
        revalidatePath('/dashboard/brands')
        return { success: true, error: '', response: response }
    } catch (error) {
        if (error instanceof Error) {
            return { success: false, error: error.message }

        }
        return { success: false, error: 'Error al crear marca' }
    }
}