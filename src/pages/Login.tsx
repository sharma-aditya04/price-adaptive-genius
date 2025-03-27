
import React, { useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { Eye, EyeOff, Lock, LogIn, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { toast } from "sonner";

const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [showPassword, setShowPassword] = useState(false);
  const [isSignUp, setIsSignUp] = useState(false);
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    
    try {
      // Simulate authentication
      await new Promise(resolve => setTimeout(resolve, 1500));
      
      // Success notification
      toast.success(isSignUp ? "Account created successfully!" : "Login successful!", {
        description: `Welcome back, ${email.split('@')[0]}`,
      });
      
      // Redirect to dashboard
      navigate("/");
    } catch (error) {
      toast.error("Authentication failed", {
        description: "Please check your credentials and try again.",
      });
    } finally {
      setIsLoading(false);
    }
  };

  const toggleView = () => {
    setIsSignUp(!isSignUp);
    setEmail("");
    setPassword("");
  };

  return (
    <div className="min-h-screen bg-gradient-to-b from-gray-50 to-gray-100 flex flex-col items-center justify-center p-4">
      <Link 
        to="/" 
        className="absolute top-8 left-8 text-gray-600 hover:text-gray-900 transition-colors"
      >
        ← Back to Home
      </Link>
      
      <div className="w-full max-w-md">
        <Card className="border-gray-200 shadow-lg animate-fade-in">
          <CardHeader className="space-y-1 text-center">
            <div className="mx-auto bg-primary/10 p-3 rounded-full w-16 h-16 flex items-center justify-center mb-2">
              <LogIn className="h-8 w-8 text-primary" />
            </div>
            <CardTitle className="text-2xl font-bold">{isSignUp ? "Create an Account" : "Welcome Back"}</CardTitle>
            <CardDescription>
              {isSignUp 
                ? "Sign up to start optimizing your pricing strategy" 
                : "Enter your credentials to access your account"}
            </CardDescription>
          </CardHeader>
          
          <form onSubmit={handleSubmit}>
            <CardContent className="space-y-4">
              <div className="space-y-2">
                <Label htmlFor="email">Email</Label>
                <div className="relative">
                  <User className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="email"
                    type="email"
                    placeholder="you@example.com"
                    className="pl-9"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                  />
                </div>
              </div>
              
              <div className="space-y-2">
                <Label htmlFor="password">Password</Label>
                <div className="relative">
                  <Lock className="absolute left-3 top-3 h-4 w-4 text-gray-400" />
                  <Input
                    id="password"
                    type={showPassword ? "text" : "password"}
                    placeholder={isSignUp ? "Create a password" : "Enter your password"}
                    className="pl-9 pr-9"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                    minLength={6}
                  />
                  <button
                    type="button"
                    onClick={() => setShowPassword(!showPassword)}
                    className="absolute right-3 top-3 text-gray-400 hover:text-gray-600 focus:outline-none"
                    aria-label={showPassword ? "Hide password" : "Show password"}
                  >
                    {showPassword ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
                  </button>
                </div>
              </div>

              {isSignUp && (
                <div className="text-sm text-gray-500">
                  Password must be at least 6 characters long
                </div>
              )}
              
              {!isSignUp && (
                <div className="flex justify-end">
                  <Link 
                    to="#" 
                    className="text-sm text-primary hover:underline"
                  >
                    Forgot your password?
                  </Link>
                </div>
              )}
            </CardContent>
            
            <CardFooter className="flex flex-col space-y-4">
              <Button 
                type="submit" 
                className="w-full" 
                disabled={isLoading}
              >
                {isLoading ? (
                  <div className="flex items-center justify-center gap-2">
                    <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
                    <span>{isSignUp ? "Creating account..." : "Logging in..."}</span>
                  </div>
                ) : (
                  <span>{isSignUp ? "Create Account" : "Sign In"}</span>
                )}
              </Button>
              
              <div className="text-center text-sm">
                {isSignUp ? "Already have an account? " : "Don't have an account? "}
                <button
                  type="button"
                  onClick={toggleView}
                  className="text-primary hover:underline font-medium"
                >
                  {isSignUp ? "Sign in" : "Create one"}
                </button>
              </div>
            </CardFooter>
          </form>
        </Card>
      </div>
      
      <p className="mt-8 text-center text-sm text-gray-500">
        Price Adaptive Genius — Optimize your pricing strategy with AI
      </p>
    </div>
  );
};

export default Login;
