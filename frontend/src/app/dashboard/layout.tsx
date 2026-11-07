import React from "react";
import { getUser } from "@/lib/auth";
import { redirect } from "next/navigation";
import { Sidebar } from "@/components/dashboard/sidebar";
import { MobileSidebar } from "@/components/dashboard/mobile-sidebar";
import { Toaster } from "@/components/ui/toast";

export default async function DashboardLayout({
    children,
}: {
    children: React.ReactNode;
}) {
    const user = await getUser();
    if (!user) {
        redirect('/login');
    }
    console.log(user);
    return (
        <div className="flex h-screen overflow-hidden">
            <Sidebar username={user.username} />
            <div className="flex flex-1 flex-col overflow-hidden">
                <MobileSidebar username={user.username} />
                <main className="flex-1 overflow-y-auto">
                    <div className="container max-w-full px-4 py-6">
                        {children}
                        <Toaster />
                    </div>
                </main>
            </div>
        </div>
    )
}