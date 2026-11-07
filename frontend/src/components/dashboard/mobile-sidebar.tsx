'use client'
import { cn } from '@/lib/utils';

import { Badge, Tag, LogOut, Menu } from "lucide-react";
import { usePathname } from "next/navigation";
import { Button } from "@/components/ui/button";
import Link from "next/link";
import { ModeToggle } from "@/components/mode-toggle";
import { logoutAction } from '@/actions/auth';

import {
    Sheet,
    SheetClose,
    SheetContent,
    SheetDescription,
    SheetFooter,
    SheetHeader,
    SheetTitle,
    SheetTrigger,
} from "@/components/ui/sheet";
import { useState } from "react";

interface SidebarProps {
    username: string;
}

const menuItems = [
    {
        title: "Brands",
        href: "/dashboard/brands",
        icon: Badge
    },
    {
        title: "Products",
        href: "/dashboard/products",
        icon: Tag
    }
]

export function MobileSidebar({ username }: SidebarProps) {
    const pathname = usePathname();
    const [open, setOpen] = useState(false);

    return (
        <div className="lg:hidden">
            <header className="sticky top-0 z-50 border-b">
                <div className="flex h-16 items-center justify-between px-4">
                    <h1 className='text-xl font-bold'>My <span className='text-primary'>API</span></h1>
                    <Sheet open={open} onOpenChange={setOpen} >
                        <SheetTrigger render={<Button variant={'ghost'} size={'icon'}><Menu className="h-6 w-6" /></Button>} />

                        <SheetContent>
                            <SheetHeader className='border-b'>
                                <SheetTitle className="text-xl font-bold">
                                    Menu
                                </SheetTitle>
                            </SheetHeader>

                            <nav className="flex flex-col flex-1 p-4 space-y-4">
                                {menuItems.map(item => {
                                    const Icon = item.icon
                                    const isActivePath = pathname === item.href;

                                    return (
                                        <Link
                                            href={item.href}
                                            key={item.title}
                                            className={cn(
                                                "flex items-center gap-3 px-3 py-2 text-sm transition-all duration-300",
                                                isActivePath ? "bg-accent text-accent-foreground" : "hover:bg-sidebar-accent"
                                            )}
                                        >
                                            <Icon
                                                className="w-5 h-5"
                                            />
                                            {item.title}
                                        </Link>
                                    )
                                })}
                            </nav>
                            <div className='border-t p-4 w-full'>
                                <form action={logoutAction}>
                                    <Button
                                        type='submit'
                                        variant={'ghost'}
                                        className={'w-full justify-start items-center'}
                                    >
                                        <LogOut className='w-5 h-5' />
                                        Logout
                                    </Button>
                                </form>
                                <ModeToggle />
                            </div>
                        </SheetContent>
                    </Sheet>
                </div>
            </header>
        </div>
    )
}