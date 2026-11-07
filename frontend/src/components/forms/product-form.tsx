'use client';
import React, { useState } from "react";
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog";
import {
    Select,
    SelectContent,
    SelectGroup,
    SelectItem,
    SelectTrigger,
    SelectValue,
    SelectLabel
} from "@/components/ui/select";
import { Button } from "../ui/button";
import { Plus } from "lucide-react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { createProduct } from "@/actions/products";
import { useRouter } from "next/navigation";
import { Brand, BrandsList } from "@/lib/types";
import { Field } from "@/components/ui/field";

interface ProductFormProps {
    brands: Brand[]
}

export function ProductForm({ brands }: ProductFormProps) {
    const [open, setOpen] = useState(false);
    const [selectedBrand, setSelectedBrand] = useState(null);
    const router = useRouter();

    async function handleCreateProduct(e: React.SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const result = await createProduct(formData);
        if (result.success) {
            setOpen(false);
            setSelectedBrand(null);
            router.refresh();
            return;
        } else {
            console.log(result.error);
        }
    }

    const items = brands.map((brand) => (
        {
            label: brand.name,
            value: brand.id
        }
    ))
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger render={<Button></Button>}>
                <Plus /><span>Nuevo Producto</span>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>Nuevo Producto</DialogTitle>
                </DialogHeader>
                <form className="space-y-4" onSubmit={handleCreateProduct}>
                    <Label htmlFor="name">
                        Producto
                    </Label>
                    <Input
                        id="name"
                        name="name"
                        required
                        placeholder="Ej: Perfume-x"
                    />
                    <Label htmlFor="brand">
                        Marca
                    </Label>
                    <Field>
                        <Select
                            items={items}
                            id="brand"
                            name="brand"
                            value={selectedBrand}
                            onValueChange={setSelectedBrand}
                            required
                        >
                            <SelectTrigger className="w-full max-w-48" aria-invalid>
                                <SelectValue placeholder="Elige una marca" />
                            </SelectTrigger>
                            <SelectContent>
                                <SelectGroup>
                                    <SelectLabel>Marcas</SelectLabel>
                                    {brands.map((brand) => (
                                        <SelectItem key={brand.id} value={brand.id}>
                                            {brand.name}
                                        </SelectItem>
                                    ))}
                                </SelectGroup>
                            </SelectContent>
                        </Select>

                    </Field>
                    <Button
                        type="submit"
                        className="w-full"
                    >
                        Crear Producto
                    </Button>
                </form>
            </DialogContent>
        </Dialog>
    )
}
