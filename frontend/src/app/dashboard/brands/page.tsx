import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter, CardAction } from "@/components/ui/card";
import { apiClient } from "@/lib/api";
import { getToken } from "@/lib/auth";
import { BrandsList } from "@/lib/types";
import { BrandForm } from "@/components/forms/brand-form";

export default async function Brands() {
    const token = await getToken();
    const data = await apiClient<BrandsList>('/api/v1/brands', {
        token: token!
    })
    const brands = data.brands;
    console.log(brands)
    return (
        <div className="space-y-4 sm:space-y-6">
            <div className="flex sm:items-center justify-between gap-4">
                <div>
                    <h1 className="text-2xl sm:text-3xl font-bold">Brands</h1>
                    <p className="text-sm sm:text-base mt-1">Brands page</p>
                </div>
                <BrandForm />
            </div>

            {brands.length !== 0 && (
                <div className="grid md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4 ">
                    {brands.map(brand => (
                        <Card key={brand.id} className="gap-2">
                            <CardHeader>
                                <CardTitle className="text-xl">{brand.name}</CardTitle>
                            </CardHeader>
                            <CardContent>
                                <p className="text-sm">ID: {brand.id}</p>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            )}

        </div>
    )
}