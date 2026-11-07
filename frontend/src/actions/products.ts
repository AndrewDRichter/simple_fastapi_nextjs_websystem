'use server'
import { apiClient } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { Product } from "@/lib/types";
import { revalidatePath } from "next/cache";

export async function createProduct(formData: FormData) {
    try {
        const name = formData.get('name');
        const brand_id = formData.get('brand')

        const token = await getToken();

        if (!token) {
            return { success: false, error: 'Error al crear producto' }
        }

        const data = {
            name: name,
            brand_id: brand_id
        }
        console.log(data)

        const response = await apiClient<Product>('/api/v1/products/', {
            method: 'POST',
            body: JSON.stringify(data),
            token: token
        })
        revalidatePath('/dashboard/products')
        return { success: true, error: '', response: response }
    } catch (error) {
        if (error instanceof Error) {
            console.log(error)
            return { success: false, error: error.message }

        }
        return { success: false, error: 'Error al crear producto' }
    }
}

export async function deleteProduct(productId: number) {
    try {
        if (!productId) {
            return { success: false, error: "Error al apagar producto" }
        }

        const token = await getToken();
        if (!token) {
            return { success: false, error: 'Error al apagar producto' }
        }
        const url = `/api/v1/products/${productId}`

        await apiClient<void>(url, {
            method: 'DELETE',
            token: token,
        })

        revalidatePath('/dashboard/products')
        return { success: true, error: '' }
    } catch (error) {
        if (error instanceof Error) {
            console.log(error)
            console.log('erroo')
            return { success: false, error: error.message }

        }
        return { success: false, error: 'Error al apagar producto' }
    }
}