'use client'
import { cn } from '@/lib/utils';
import { Badge, Tag, LogOut } from "lucide-react";
import Link from "next/link";
import { usePathname } from "next/navigation";

import { ThemeProvider } from "@/components/theme-provider"
import { ModeToggle } from "@/components/mode-toggle";
import { Button } from '@/components/ui/button';
import { logoutAction } from '@/actions/auth';

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

export function Sidebar({ username }: SidebarProps) {
    const pathname = usePathname();
    console.log(pathname)

    return (
        <aside className=" hidden lg:flex flex-col h-screen w-64 border-r border-sidebar-border bg-sidebar">
            {/* HEADER */}
            <div className="border-b p-6">
                <h2 className="text-4xl font-bold">My <span className="text-primary">API</span></h2>
                <p className="text-md text-gray-600 dark:text-gray-400">Hola, {username}</p>
            </div>
            {/* MENU */}
            <nav className="flex-1 p-4 space-y-4">
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
            <div className='border-t p-4'>
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
        </aside>
    )
}