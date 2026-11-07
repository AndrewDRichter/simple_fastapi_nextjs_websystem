import {
    Card,
    CardAction,
    CardContent,
    CardDescription,
    CardFooter,
    CardHeader,
    CardTitle,
} from "@/components/ui/card"
import { apiClient } from "@/lib/api"
import { getToken } from "@/lib/auth"
import { BrandsList, ProductsList } from "@/lib/types";
import { ProductForm } from "@/components/forms/product-form";
import { DeleteProductButton } from "@/components/forms/delete-button";

export default async function Products() {
    const token = await getToken();
    const data = await apiClient<ProductsList>('/api/v1/products/', {
        token: token!
    })
    const products = data.products;
    const brand_data = await apiClient<BrandsList>('/api/v1/brands/', {
        token: token!
    })
    const brands = brand_data.brands;
    return (
        <div className="space-y-4 sm:space-y-6">
            <div className="flex sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl sm:text-3xl font-bold">Productos</h1>
                    <p className="text-sm sm:text-base mt-1">Página de productos</p>
                </div>
                <ProductForm brands={brands} />
            </div>

            {products.length !== 0 && (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 ">
                    {products.map(product => (
                        <Card key={product.id} className="gap-2">
                            <CardHeader className="flex justify-between">
                                <CardTitle className="text-xl">{product.name}</CardTitle>
                                <DeleteProductButton productId={product.id} />
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm">ID: {product.id}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

        </div>
    )
}