'use client';
import { deleteProduct } from "@/actions/products";
import { Button } from "@/components/ui/button";
import { Trash } from "lucide-react";
import { useRouter } from "next/navigation";
import {
    AlertDialog,
    AlertDialogAction,
    AlertDialogCancel,
    AlertDialogContent,
    AlertDialogDescription,
    AlertDialogFooter,
    AlertDialogHeader,
    AlertDialogTitle,
    AlertDialogTrigger,
} from "@/components/ui/alert-dialog"
import { useState } from "react";

interface DeleteProductButtonProps {
    productId: number;
}

export function DeleteProductButton({ productId }: DeleteProductButtonProps) {
    const router = useRouter();
    const [alertTriggered, setAlertTriggered] = useState(false);

    async function handleDeleteProduct() {
        if (!alertTriggered) {

        }
        const result = await deleteProduct(productId);

        if (result.success) {
            router.refresh();
            return;
        }

        if (result.error !== "") {
            console.log(result);
        }
    }
    return (
        <AlertDialog>
            <AlertDialogTrigger render={<Button variant={'destructive'}></Button>}>
                <Trash />
            </AlertDialogTrigger>
            <AlertDialogContent>
                <AlertDialogHeader>
                    <AlertDialogTitle>
                        Estáis seguro que desea apagar este producto?
                    </AlertDialogTitle>
                    <AlertDialogDescription>
                        Esta accion apagará este registro permanentemente bla bla.
                    </AlertDialogDescription>
                </AlertDialogHeader>
                <AlertDialogFooter>
                    <AlertDialogCancel>Cancelar</AlertDialogCancel>
                    <AlertDialogAction onClick={handleDeleteProduct} variant={'destructive'}>Apagar</AlertDialogAction>
                </AlertDialogFooter>
            </AlertDialogContent>
        </AlertDialog>
    )
}