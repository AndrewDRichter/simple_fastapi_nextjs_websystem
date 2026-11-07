
export interface User {
    id: string;
    username: string;
    email: string;
    created_at: Date;
    updated_at: Date;
}

export interface LoginResponse {
    access_token: string;
    token_type: string;
}

export interface Brand {
    id: number,
    name: string,
    user: User,
    created_at: Date,
    updated_at: Date
}

export interface BrandsList {
    brands: Brand[]
}

export interface Product {
    id: number,
    name: string,
    user: User,
    brand: Brand,
    created_at: Date,
    updated_at: Date
}

export interface ProductsList {
    products: Product[]
}