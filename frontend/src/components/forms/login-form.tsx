'use client';

import { useActionState, useEffect } from 'react';
import {
    Card,
    CardHeader,
    CardTitle,
    CardContent,
    CardDescription,
    CardFooter,
} from '@/components/ui/card';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import Link from 'next/link';

import { loginAction } from '@/actions/auth';
import { useRouter } from 'next/navigation';

export function LoginForm() {

    const [state, formAction, isPending] = useActionState(loginAction, null)
    const router = useRouter();

    useEffect(() => {
        if (state?.success && state?.redirectTo) {
            router.replace(state.redirectTo)
        }
    }, [state, router])

    return (
        <Card className='w-full max-w-md mx-auto'>
            <CardHeader>
                <CardTitle className='text-center text-3xl sm:text-4xl md:text-5xl'>
                    My <span className='text-primary'>API</span>
                </CardTitle>
                <CardDescription>
                    Log into your account
                </CardDescription>
            </CardHeader>
            <CardContent>
                <form className='space-y-4' action={formAction}>
                    <div className='space-y-2'>
                        <Label htmlFor='email'>Email</Label>
                        <Input
                            type='email'
                            id='email'
                            name='email'
                            placeholder='Your Email'
                            required
                        />
                    </div>
                    <div className='space-y-2'>
                        <Label htmlFor='password'>Password</Label>
                        <Input
                            type='password'
                            id='password'
                            name='password'
                            placeholder='Your password'
                            required
                        />
                    </div>
                    <Button type='submit' className={'w-full'}>
                        {isPending ? 'Loggin into your account...' : 'Log in'}
                    </Button>
                    {state?.error && (
                        <div className='w-full text-center'>
                            <span className='text-sm text-destructive'>
                                {state.error}
                            </span>
                        </div>
                    )}
                </form>
            </CardContent>
            <CardFooter>
                <p className='w-full text-center'>
                    Do not have an account yet? <Link className='text-primary hover:text-foreground' href={'/register'}>Sign up</Link>
                </p>
            </CardFooter>
        </Card>
    )
}