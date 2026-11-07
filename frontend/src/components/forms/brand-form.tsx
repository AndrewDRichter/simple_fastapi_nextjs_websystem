'use client'
import React, { useState } from "react"
import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
} from "@/components/ui/dialog"
import { Button } from "../ui/button";
import { Plus } from "lucide-react";
import { Label } from "../ui/label";
import { Input } from "../ui/input";
import { createBrand } from "@/actions/brands";
import { useRouter } from "next/navigation";

export function BrandForm() {
    const [open, setOpen] = useState(false);
    const router = useRouter();

    async function handleCreateBrand(e: React.SubmitEvent<HTMLFormElement>) {
        e.preventDefault();
        const formData = new FormData(e.currentTarget);
        const result = await createBrand(formData);
        if (result.success) {
            setOpen(false);
            router.refresh();
            return;
        } else {
            console.log(result.error);
        }
    }
    return (
        <Dialog open={open} onOpenChange={setOpen}>
            <DialogTrigger render={<Button></Button>}>
                <Plus /><span>New Brand</span>
            </DialogTrigger>
            <DialogContent>
                <DialogHeader>
                    <DialogTitle>New Brand Form</DialogTitle>
                </DialogHeader>
                <form className="space-y-4" onSubmit={handleCreateBrand}>
                    <Label htmlFor="name">
                        Brand name
                    </Label>
                    <Input
                        id="name"
                        name="name"
                        required
                        placeholder="Enter brand name"
                    />
                    <Button
                        type="submit"
                        className="w-full"
                    >
                        Create Brand
                    </Button>
                </form>
            </DialogContent>
        </Dialog>
    )
}
