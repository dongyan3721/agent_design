import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import { Header, Sidebar } from "@/components/layout";
import { ROUTES, withLocale } from "@/lib/constants";

export default async function DashboardLayout({
  children,
  params,
}: {
  children: React.ReactNode;
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;
  const accessToken = (await cookies()).get("access_token")?.value;
  if (!accessToken) {
    redirect(withLocale(ROUTES.LOGIN, locale));
  }

  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <div className="flex min-w-0 flex-1 flex-col">
        <Header />
        <main className="flex-1 overflow-auto p-3 sm:p-6">{children}</main>
      </div>
    </div>
  );
}
