import Link from "next/link";
import { Button, Card, CardHeader, CardTitle, CardContent } from "@/components/ui";
import { ROUTES, withLocale } from "@/lib/constants";

export default async function HomePage({
  params,
}: {
  params: Promise<{ locale: string }>;
}) {
  const { locale } = await params;

  return (
    <div className="min-h-screen bg-background">
      <div className="container mx-auto py-16 px-4">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold mb-4">
            med_agent
          </h1>
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
            medagent
          </p>
        </div>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 max-w-5xl mx-auto">
          <Card>
            <CardHeader>
              <CardTitle>Authentication</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-4 text-muted-foreground">
                Secure JWT-based authentication system
              </p>
              <div className="flex gap-2">
                <Button asChild>
                  <Link href={withLocale(ROUTES.LOGIN, locale)}>Login</Link>
                </Button>
                <Button variant="outline" asChild>
                  <Link href={withLocale(ROUTES.REGISTER, locale)}>Register</Link>
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>AI Assistant</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-4 text-muted-foreground">
                Chat with our AI assistant powered by PydanticAI
              </p>
              <Button asChild>
                <Link href={withLocale(ROUTES.CHAT, locale)}>Start Chat</Link>
              </Button>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle>Dashboard</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="mb-4 text-muted-foreground">
                View your dashboard and manage your account
              </p>
              <Button variant="outline" asChild>
                <Link href={withLocale(ROUTES.DASHBOARD, locale)}>Go to Dashboard</Link>
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
