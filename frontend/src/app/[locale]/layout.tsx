import { notFound } from "next/navigation";
import { Providers } from "../providers";
export default async function LocaleLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;  // i18n disabled - just render with providers
  return <Providers>{children}</Providers>;}
