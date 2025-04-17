import { envConfig } from '@/config';
import axios, { AxiosRequestConfig, AxiosResponse, isAxiosError } from 'axios';
import { getServerSession } from 'next-auth';
import { getSession } from 'next-auth/react';
import { authOptions } from './auth';

type ApiResult<T> = {
	data?: T;
	error?: {
		message: string;
		status: number;
		details?: Record<string, unknown>;
		validationErrors?: unknown[];
	};
};

export class ApiClient {
	static async request<T>(config: AxiosRequestConfig): Promise<ApiResult<T>> {
		try {
			const isServer = typeof window === 'undefined';
			const session = isServer ? await getServerSession(authOptions) : await getSession();

			const client = axios.create({
				baseURL: envConfig.API_URL,
				headers: {
					'Content-Type': 'application/json',
					Authorization: `Bearer ${session?.user.token}`,
				},
			});

			// Log outgoing request for debugging
			console.log(`🛎️ API REQUEST: ${config.method?.toUpperCase()} ${config.url}`);
			if (config.data) {
				console.log('🛎️ Request data (partial):', {
					...config.data,
					// Don't log full email content to keep logs clean
					ratedEmails: config.data.ratedEmails ? `[${config.data.ratedEmails.length} emails]` : undefined,
				});
			}

			const response: AxiosResponse<T> = await client.request(config);
			return { data: response.data };
		} catch (err) {
			if (isAxiosError(err)) {
				console.error(`❌ API ERROR: ${err.message}`);

				if (err.response?.status === 422) {
					console.error('❌ VALIDATION ERROR:', err.response.data);

					let message = 'Validation error';
					let validationErrors = [];

					// Handle Pydantic validation errors
					if (err.response?.data?.detail && Array.isArray(err.response.data.detail)) {
						validationErrors = err.response.data.detail;
						message = 'Form validation failed, please check your inputs';

						// Log each validation error in detail
						console.error('❌ VALIDATION ERRORS DETAILS:');
						err.response.data.detail.forEach(
							(error: { loc?: string[]; msg?: string; type?: string }, index: number) => {
								console.error(`Error ${index + 1}:`, {
									field: error.loc?.join('.'),
									message: error.msg,
									type: error.type,
								});
							}
						);
					} else {
						message = Object.values(err.response?.data.data || {}).join(', ') || 'Validation error';
					}

					return {
						error: {
							message,
							details: err.response?.data.data,
							status: err.response?.status || 500,
							validationErrors,
						},
					};
				}

				return {
					error: {
						message: err.response?.data.message || 'Server error',
						details: err.response?.data.data,
						status: err.response?.status || 500,
					},
				};
			}

			console.error('❌ UNKNOWN API ERROR:', err);
			return {
				error: {
					message: 'An unknown error occurred',
					status: 500,
				},
			};
		}
	}

	static async get<T>(url: string, params?: Record<string, unknown>): Promise<ApiResult<T>> {
		return this.request<T>({ method: 'GET', url, params });
	}

	static async post<T, D = unknown>(url: string, data?: D): Promise<ApiResult<T>> {
		return this.request<T>({ method: 'POST', url, data });
	}

	static async put<T, D = unknown>(url: string, data?: D): Promise<ApiResult<T>> {
		return this.request<T>({ method: 'PUT', url, data });
	}

	static async patch<T, D = unknown>(url: string, data?: D): Promise<ApiResult<T>> {
		return this.request<T>({ method: 'PATCH', url, data });
	}

	static async delete<T>(url: string): Promise<ApiResult<T>> {
		return this.request<T>({ method: 'DELETE', url });
	}
}
